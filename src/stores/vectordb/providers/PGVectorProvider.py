from ..VectorDBInterface import VectorDBInterface
from ..VectorDBEnums import (DistanceTypeEnums,
                             PGVectorDistanceTypeEnums,
                             PGVectorTableSchemaEnums,
                             PGVectorIndexingEnums)

from models.db_schemas import RetrievedDocument

from sqlalchemy.sql import text as sql_text

from typing import List
import json

from logging import getLogger


class PGVectorProvider(VectorDBInterface):

    def __init__(self,
                 db_client,
                 distance_method: str,
                 embedding_size: int = 768,
                 index_threshold: int = 100
                 ):

        self.db_client = db_client
        self.distance_method = PGVectorDistanceTypeEnums.COSINE.value if distance_method == DistanceTypeEnums.COSINE.value else PGVectorDistanceTypeEnums.DOT.value
        self.embedding_size = embedding_size

        self.index_threshold = index_threshold

        self.pgvector_prefix = PGVectorTableSchemaEnums._PREFIX.value

        self.get_index_name = lambda collection_name: f'{collection_name}_vector_idx'

        self.logger = getLogger('uvicorn')

    async def connect(self):

        async with self.db_client() as session:
            async with session.begin():
                await session.execute(
                    sql_text(
                        "CREATE EXTENSION IF NOT EXISTS vector"
                    )
                )

            await session.commit()

    async def disconnect(self):

        return None

    async def is_collection_exist(self, collection_name: str) -> bool:
        record = None
        async with self.db_client() as session:
            async with session.begin():
                get_table_query = sql_text(
                    "SELECT * FROM pg_tables WHERE tablename = :collection_name"
                )
                result = await session.execute(get_table_query, {"collection_name": collection_name})
                record = result.scalar_one_or_none()
        return record

    async def list_collections(self) -> List:
        records = []
        async with self.db_client() as session:
            async with session.begin():
                select_tables_query = sql_text(
                    f"SELECT tablename FROM pg_tables WHERE tablename LIKE :prefix"
                )
                result = await session.execute(select_tables_query, {"prefix": f"{self.pgvector_prefix}%"})
                records = result.scalars().all()
        return records

    async def get_collection_info(self, collection_name: str) -> dict:
        async with self.db_client() as session:
            async with session.begin():
                get_all_tables_query = sql_text(
                    f"SELECT schemaname, tablename, tableowner, tablespace, hasindexes FROM pg_tables WHERE tablename = :collection_name"
                )
                tables_result = await session.execute(get_all_tables_query, {"collection_name": collection_name})
                get_all_tables_result = tables_result.fetchall()
                if not get_all_tables_result:
                    return None

                dict_rows = [dict(row._mapping)
                             for row in get_all_tables_result]

                get_collection_rows_query = sql_text(
                    f"SELECT COUNT(*) FROM {collection_name}"
                )
                rows_result = await session.execute(get_collection_rows_query)
                get_collection_rows_result = rows_result.scalar_one()

                return {
                    'table_info': dict_rows,
                    'row_count': get_collection_rows_result
                }

    async def delete_collection(self, collection_name: str):
        async with self.db_client() as session:
            async with session.begin():
                drop_table_query = sql_text(
                    f'DROP TABLE IF EXISTS {collection_name}'
                )
                await session.execute(drop_table_query)
            await session.commit()
        return True

    async def create_collection(self, collection_name: str,
                                embedding_dim: int,
                                do_reset: bool = False):
        if do_reset:
            self.logger.info(f'Reseting {collection_name}')
            _ = await self.delete_collection(collection_name=collection_name)
        is_collection_exist = await self.is_collection_exist(collection_name=collection_name)
        if not is_collection_exist:
            self.logger.info(
                f'Creating collection {collection_name} with embedding dimension {embedding_dim}')
            async with self.db_client() as session:
                async with session.begin():
                    create_table_query = sql_text(
                        f'CREATE TABLE "{collection_name}" ('
                        f'{PGVectorTableSchemaEnums.ID.value} bigserial PRIMARY KEY, '
                        f'{PGVectorTableSchemaEnums.VECTOR.value} vector({embedding_dim}), '
                        f'{PGVectorTableSchemaEnums.TEXT.value} text, '
                        f'{PGVectorTableSchemaEnums.METADATA.value} jsonb DEFAULT \'{{}}\', '
                        f'{PGVectorTableSchemaEnums.CHUNK_ID.value} integer, '
                        f'foreign key ({PGVectorTableSchemaEnums.CHUNK_ID.value}) references chunks(chunk_id)'
                        ')'
                    )
                    await session.execute(create_table_query)
                await session.commit()
            return True

    async def is_index_existed(self, collection_name: str):
        index_name = self.get_index_name(collection_name=collection_name)
        async with self.db_client() as session:
            async with session.begin():
                check_index_occurence = sql_text(
                    f"SELECT 1 FROM pg_indexes WHERE indexname = :index_name AND tablename = :collection_name"
                )
                result = await session.execute(check_index_occurence, {"index_name": index_name, "collection_name": collection_name})
                check_result = result.scalar_one_or_none()
                return bool(check_result)

    async def reset_vector_index(self,
                                 collection_name: str,
                                 indexing_type: str = PGVectorIndexingEnums.HNSW.value):

        index_name = self.get_index_name(collection_name=collection_name)

        self.logger.info(
            f'Reseting the index {index_name} from {collection_name}')

        async with self.db_client() as session:
            async with session.begin():

                reset_vector_index_query = sql_text(
                    f'DROP INDEX IF EXISTS {index_name}'
                )

                _ = await session.execute(reset_vector_index_query)

            await session.commit()

        return await self.create_vector_index(collection_name=collection_name, indexing_type=indexing_type)

    async def create_vector_index(self,
                                  collection_name: str,
                                  indexing_type: str = PGVectorIndexingEnums.HNSW.value):

        is_index_existed = await self.is_index_existed(collection_name=collection_name)

        if is_index_existed:
            return False

        async with self.db_client() as session:
            async with session.begin():

                count_rows_query = sql_text(
                    f'SELECT COUNT(*) FROM {collection_name}'
                )

                count_result = await session.execute(count_rows_query)
                row_count = count_result.scalar_one()

                if row_count < self.index_threshold:
                    return False

                index_name = self.get_index_name(
                    collection_name=collection_name)

                self.logger.info(
                    f"Starting vector index creation: index='{index_name}', table='{collection_name}', type='{indexing_type}, distance-method={self.distance_method}'")

                create_index_query = sql_text(
                    f'CREATE INDEX {index_name} ON {collection_name} USING {indexing_type} '
                    f'({PGVectorTableSchemaEnums.VECTOR.value} {self.distance_method}) '
                )

                await session.execute(create_index_query)

            await session.commit()

        self.logger.info(
            f"Successfully finished vector index creation: index='{index_name}', table='{collection_name}', type='{indexing_type}, distance-method={self.distance_method}'")

        return True

    async def insert_one(self,
                         collection_name: str,
                         vector: List,
                         text: str,
                         metadata: str = None,
                         vector_id: str = None):
        is_collection_exists = await self.is_collection_exist(collection_name=collection_name)
        if not is_collection_exists:
            self.logger.info(
                f'Can\'t insert to non-existed collection : {collection_name}')
            return False
        if not vector_id:
            self.logger.info('In insertion, vector_id is not provided')
            return False
        metadata_json = json.dumps(
            {'metadata': metadata}, ensure_ascii=False) if metadata else '{}'
        async with self.db_client() as session:
            async with session.begin():
                insert_one_query = sql_text(
                    f'INSERT INTO "{collection_name}" '
                    f'({PGVectorTableSchemaEnums.TEXT.value}, '
                    f'{PGVectorTableSchemaEnums.VECTOR.value}, '
                    f'{PGVectorTableSchemaEnums.METADATA.value}, '
                    f'{PGVectorTableSchemaEnums.CHUNK_ID.value}) '
                    'VALUES (:text, :vector, :metadata, :vector_id)'
                )
                insert_one_result = await session.execute(
                    insert_one_query,
                    {
                        'text': text,
                        'vector': '[' + ', '.join([str(v) for v in vector]) + ']',
                        'metadata': metadata_json,
                        'vector_id': vector_id
                    }
                )
            await session.commit()
            self.logger.info(
                f'Successfully inserted one document into {collection_name}')

        _ = await self.create_vector_index(collection_name=collection_name)

        return True

    async def insert_batch(self,
                           collection_name: str, vectors: List,
                           texts: List, metadata: List = None,
                           vector_ids: List = None, batch_size: int = 80):
        is_collection_exists = await self.is_collection_exist(collection_name=collection_name)
        if not is_collection_exists:
            self.logger.info(
                f'Can\'t insert to non-existed collection : {collection_name}')
            return False
        if len(vector_ids) != len(texts):
            self.logger.info(
                f'The size of vector_ids must be equal to the size of the texts')
            return False
        if not metadata:
            metadata = [None]*len(texts)
        elif len(metadata) < len(texts):
            diff = len(texts)-len(metadata)
            metadata.extend([None]*diff)
        async with self.db_client() as session:
            async with session.begin():
                for i in range(0, len(texts), batch_size):
                    batch_vectors = vectors[i:i+batch_size]
                    batch_texts = texts[i:i+batch_size]
                    batch_vector_ids = vector_ids[i:i+batch_size]
                    batch_metadata = metadata[i:i+batch_size]
                    values = []
                    for _vector_ids, _text, _vector, _metadata in zip(batch_vector_ids, batch_texts, batch_vectors, batch_metadata):

                        metadata_json = json.dumps(
                            {'metadata': _metadata}, ensure_ascii=False) if _metadata else '{}'
                        values.append(
                            {
                                'text': _text,
                                'vector': '[' + ', '.join([str(v) for v in _vector]) + ']',
                                'metadata': metadata_json,
                                'vector_id': _vector_ids
                            }
                        )
                    batch_insert_query = sql_text(
                        f'INSERT INTO "{collection_name}" '
                        f'({PGVectorTableSchemaEnums.TEXT.value}, '
                        f'{PGVectorTableSchemaEnums.VECTOR.value}, '
                        f'{PGVectorTableSchemaEnums.METADATA.value}, '
                        f'{PGVectorTableSchemaEnums.CHUNK_ID.value}) '
                        'VALUES (:text, :vector, :metadata, :vector_id)'
                    )
                    batch_insert_result = await session.execute(
                        batch_insert_query,
                        values
                    )
            await session.commit()

        _ = await self.create_vector_index(collection_name=collection_name)
        return True

    async def search_by_vector(self,
                               vector: List,
                               collection_name: str,
                               top_k: int) -> List[RetrievedDocument]:

        is_collection_exists = await self.is_collection_exist(collection_name=collection_name)

        if not is_collection_exists:
            self.logger.info(
                f"Can't search on non-existed collection : {collection_name}")
            return False

        str_query_vector = '[' + ', '.join([str(v) for v in vector]) + ']'

        async with self.db_client() as session:
            async with session.begin():

                search_query = sql_text(
                    f'SELECT {PGVectorTableSchemaEnums.TEXT.value} as text, {PGVectorTableSchemaEnums.METADATA.value} as metadata ,1-({PGVectorTableSchemaEnums.VECTOR.value} <=> :vector) as score '
                    f'FROM {collection_name} '
                    f'ORDER BY score DESC '
                    f'LIMIT {top_k}'
                )

                search_results = await session.execute(
                    search_query,
                    {
                        'vector': str_query_vector
                    }
                )
                all_results = search_results.fetchall()

                return [
                    RetrievedDocument(
                        text=record.text,
                        score=record.score,
                        metadata=record.metadata
                    )
                    for record in all_results
                ]

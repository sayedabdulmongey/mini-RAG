from ..VectorDBInterface import VectorDBInterface
from ..VectorDBEnums import VectorDBEnums, DistanceTypeEnums
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Record
from logging import getLogger

from models.db_schemas import RetrievedDocument

import os

from typing import List

class QdrantProvider(VectorDBInterface):

    def __init__(self, 
                 db_client: str, 
                 distance_method: str,
                 embedding_size: int = 768,
                 index_threshold: int = 100):

        self.client = None

        self.db_client = db_client

        self.distance_method = None

        self.embedding_size=embedding_size

        if distance_method == DistanceTypeEnums.COSINE.value:
            self.distance_method = Distance.COSINE
        elif distance_method == DistanceTypeEnums.DOT.value:
            self.distance_method = Distance.DOT

        self.logger = getLogger('uvicorn')

    async def connect(self):
        self.client = QdrantClient(path=self.db_client)

    async def disconnect(self):
        self.client = None

    async def is_collection_exist(self, collection_name: str):
        return self.client.collection_exists(collection_name=collection_name)

    async def list_collections(self):
        return self.client.get_collections()

    async def get_collection_info(self, collection_name: str):
        return self.client.get_collection(collection_name=collection_name)

    async def delete_collection(self, collection_name: str):
        if self.is_collection_exist(collection_name=collection_name):
            return self.client.delete_collection(collection_name=collection_name)

    async def create_collection(self, collection_name: str,
                                embedding_dim: int,
                                do_reset: bool = False):

        if do_reset:
            self.logger.info(f"Reset flag is True. Deleting collection '{collection_name}' if it exists.")
            _ = await self.delete_collection(collection_name=collection_name)

        exists = await self.is_collection_exist(collection_name=collection_name)
        if not exists:
            self.logger.info(f"Collection '{collection_name}' does not exist. Creating new collection.")
            _ = self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=embedding_dim,
                    distance=self.distance_method
                ),
            )
            self.logger.info(f"Collection '{collection_name}' created successfully.")
            return True
        else:
            self.logger.info(f"Collection '{collection_name}' already exists. No action taken.")
        return False

    async def insert_one(self, collection_name: str, vector: List,
                         text: str, metadata: str = None, vector_id: str = None):

        if not self.is_collection_exist(collection_name=collection_name):
            self.logger.error(
                f'Cannot insert record to non-existing collection: {collection_name}')
            return None
        try:
            _ = self.client.upload_records(
                collection_name=collection_name,
                records=[
                    Record(
                        id=[vector_id],
                        vector=vector,
                        payload={
                            "text": text,
                            "metadata": metadata
                        }
                    )
                ]
            )
        except Exception as e:
            self.logger.error(f'Error inserting record: {e}')
            return False
        return True

    async def insert_batch(self, collection_name: str, vectors: List,
                           texts: List, metadata: List = None, vector_ids: List = None, batch_size: int = 80):

        if not self.is_collection_exist(collection_name=collection_name):
            self.logger.error(
                f'Cannot insert record to non-existing collection: {collection_name}')
            return None

        if not metadata:
            metadata = [None] * len(vectors)

        if not vector_ids:
            vector_ids = list(range(0, len(texts)))

        for i in range(0, len(vectors), batch_size):

            vector_batch = vectors[i:i+batch_size]
            text_batch = texts[i:i+batch_size]
            metadata_batch = metadata[i:i+batch_size]
            vector_id_batch = vector_ids[i:i+batch_size]
            try:
                _ = self.client.upload_records(
                    collection_name=collection_name,
                    records=[
                        Record(
                            id=vector_id_batch[idx],
                            vector=vector_batch[idx],
                            payload={
                                "text": text_batch[idx],
                                "metadata": metadata_batch[idx]
                            }
                        )
                        for idx in range(len(text_batch))
                    ]
                )
            except Exception as e:
                self.logger.error(f'Error inserting batch: {e}')
                return False

            return True

    async def search_by_vector(self, vector: list, collection_name: str, top_k: int):

        results = self.client.search(
            collection_name=collection_name,
            query_vector=vector,
            limit=top_k
        )

        if not results or len(results) == 0:
            return None

        return [
            RetrievedDocument(
                **{
                    'score': result.score,
                    'text': result.payload['text'],
                    'metadata': result.payload['metadata'],
                }
            )
            for result in results
        ]

from .BaseController import BaseController
from stores.llm import LLMFactoryProvider
from stores.vectordb import VectorDBFactoryProvider

from models.db_schemas import DataChunk

from stores.llm.LLMEnums import DocumentTypeEnums

import json
from typing import List


class NLPController(BaseController):

    def __init__(self, vectordb_client: VectorDBFactoryProvider,
                 generation_model: LLMFactoryProvider,
                 embedding_model: LLMFactoryProvider):
        super().__init__()

        self.vectordb_client = vectordb_client
        self.generation_model = generation_model
        self.embedding_model = embedding_model

    def create_collection_name(self, project_id: str):
        return f'collection_{project_id}'.strip()

    def reset_vector_db_collection(self, project_id: str):
        collection_name = self.create_collection_name(project_id=project_id)
        return self.vectordb_client.delete_collection(collection_name=collection_name)

    def get_vector_db_info(self, project_id: str):
        collection_name = self.create_collection_name(project_id=project_id)
        collection_info = self.vectordb_client.get_collection_info(
            collection_name=collection_name)

        return json.loads(
            json.dumps(collection_info, default=lambda x: x.__dict__)
        )

    def index_into_vector_db(self, project_id: str, chunks: List[DataChunk],
                             chunk_ids: List[int],
                             do_reset: bool = False):

        collection_name = self.create_collection_name(project_id=project_id)

        texts = [c.chunk_text for c in chunks]
        metadata = [c.chunk_metadata for c in chunks]
        vectors = [
            self.embedding_model.get_embedding(
                text=text, document_type=DocumentTypeEnums.DOCUMENT.value)
            for text in texts
        ]

        _ = self.vectordb_client.create_collection(
            collection_name=collection_name,
            embedding_dim=self.embedding_model.embedding_size,
            do_reset=do_reset
        )

        _ = self.vectordb_client.insert_batch(
            collection_name=collection_name,
            vectors=vectors,
            texts=texts,
            metadata=metadata,
            vector_ids=chunk_ids
        )

        return True

    def search_vector_db_collection(self, project_id: str, text: str, limit: int = 10):

        collection_name = self.create_collection_name(project_id=project_id)

        vector = self.embedding_model.get_embedding(
            text=text, document_type=DocumentTypeEnums.QUERY.value)

        if not vector or len(vector) == 0:
            return False

        results = self.vectordb_client.search_by_vector(
            vector=vector,
            collection_name=collection_name,
            top_k=limit
        )

        if not results:
            return False

        return json.loads(
            json.dumps(results, default=lambda x: x.__dict__)
        )

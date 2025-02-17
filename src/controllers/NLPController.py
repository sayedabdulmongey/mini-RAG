from .BaseController import BaseController
from stores.llm import LLMFactoryProvider
from stores.llm.templates import TemplateParser
from stores.vectordb import VectorDBFactoryProvider

from models.db_schemas import DataChunk

from stores.llm.LLMEnums import DocumentTypeEnums

import json
from typing import List


class NLPController(BaseController):

    def __init__(self, vectordb_client: VectorDBFactoryProvider,
                 generation_model: LLMFactoryProvider,
                 embedding_model: LLMFactoryProvider,
                 template_parser: TemplateParser):
        super().__init__()

        self.vectordb_client = vectordb_client
        self.generation_model = generation_model
        self.embedding_model = embedding_model
        self.template_parser = template_parser

    def create_collection_name(self, project_id: int):
        return f'collection_{project_id}'.strip()

    def reset_vector_db_collection(self, project_id: int):
        collection_name = self.create_collection_name(project_id=project_id)
        return self.vectordb_client.delete_collection(collection_name=collection_name)

    def get_vector_db_info(self, project_id: int):
        collection_name = self.create_collection_name(project_id=project_id)
        collection_info = self.vectordb_client.get_collection_info(
            collection_name=collection_name)

        return json.loads(
            json.dumps(collection_info, default=lambda x: x.__dict__)
        )

    def index_into_vector_db(self, project_id: int, chunks: List[DataChunk],
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

    def search_vector_db_collection(self, project_id: int, text: str, limit: int = 10):

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

        return results

    def answer_rag_question(self, project_id: int, query: str, limit: int = 10):

        full_prompt, chat_history, answer = None, None, None

        retrieved_documents = self.search_vector_db_collection(
            project_id=project_id,
            text=query,
            limit=limit
        )

        if not retrieved_documents or len(retrieved_documents) == 0:
            return full_prompt, chat_history, answer

        system_prompt = self.template_parser.get_template(
            group='rag',
            key='system_prompt',
        )

        documents_prompt = '\n'.join(
            [
                self.template_parser.get_template(
                    group='rag',
                    key='document_prompt',
                    vars={
                        'doc_num': idx,
                        'doc_content': self.generation_model.process_text(doc.text),
                        'doc_metadata': doc.metadata
                    }
                )
                for idx, doc in enumerate(retrieved_documents, 1)
            ]
        )

        footer_prompt = self.template_parser.get_template(
            group='rag',
            key='footer_prompt',
            vars={
                'query': query
            }
        )

        chat_history = [
            self.generation_model.construct_prompt(
                prompt=system_prompt,
                role=self.generation_model.enums.SYSTEM.value
            )
        ]

        full_prompt = '\n'.join(
            [
                documents_prompt,
                footer_prompt
            ]
        )

        answer = self.generation_model.generate_text(
            prompt=full_prompt,
            chat_history=chat_history,
        )

        return full_prompt, chat_history, answer

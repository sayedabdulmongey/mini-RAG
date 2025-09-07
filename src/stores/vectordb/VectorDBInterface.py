from abc import ABC, abstractmethod

from models.db_schemas import RetrievedDocument
from typing import List


class VectorDBInterface(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def is_collection_exist(self, collection_name: str):
        pass

    @abstractmethod
    def list_collections(self):
        pass

    @abstractmethod
    def get_collection_info(self, collection_name: str):
        pass

    @abstractmethod
    def create_collection(self, collection_name: str,
                          embedding_dim: int,
                          do_reset: bool = False):
        pass

    @abstractmethod
    def delete_collection(self, collection_name: str):
        pass

    @abstractmethod
    def insert_one(self, collection_name: str, vector: List,
                   text: str, metadata: str = None, vector_id: str = None):
        pass

    @abstractmethod
    def insert_batch(self, collection_name: str, vectors: List,
                     texts: List, metadata: List = None, vector_ids: List = None, batch_size: int = 80):
        pass

    @abstractmethod
    def search_by_vector(self, vector: List, collection_name: str, top_k: int) -> List[RetrievedDocument]:
        pass

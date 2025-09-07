from .VectorDBEnums import VectorDBEnums
from .providers import QdrantProvider, PGVectorProvider
from controllers import BaseController

from sqlalchemy.orm import sessionmaker


class VectorDBFactoryProvider():

    def __init__(self, config: dict, db_client: sessionmaker):

        self.config = config
        self.base_controller = BaseController()
        self.db_client = db_client

    def create_provider(self, provider: str):

        if provider == VectorDBEnums.QDRANT.value:
            return QdrantProvider(
                db_client=self.base_controller.get_db_path(
                    db_name=self.config.VECTOR_DB_PATH),
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD,
                embedding_size=self.config.EMBEDDING_SIZE,
                index_threshold=self.config.VECTOR_DB_PG_INDEXING_THRESHOLD
            )

        if provider == VectorDBEnums.PGVECTOR.value:
            return PGVectorProvider(
                db_client=self.db_client,
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD,
                embedding_size=self.config.EMBEDDING_SIZE,
                index_threshold=self.config.VECTOR_DB_PG_INDEXING_THRESHOLD
            )

        return None

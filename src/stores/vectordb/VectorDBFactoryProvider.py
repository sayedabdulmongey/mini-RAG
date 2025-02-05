from .VectorDBEnums import VectorDBEnums
from .providers import QdrantProvider
from controllers import BaseController


class VectorDBFactoryProvider():

    def __init__(self, config: dict):
        self.config = config

    def create_provider(self, provider: str):

        if provider == VectorDBEnums.QDRANT.value:
            return QdrantProvider(
                db_path=BaseController().get_db_path(
                    self.config.VECTOR_DB_PATH
                ),
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD,
            )

        return None

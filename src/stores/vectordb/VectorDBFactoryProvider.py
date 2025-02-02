from .VectorDBEnums import VectorDBEnums
from providers import QdrantProvider
from ...controllers import BaseController


class VectorDBFactoryProvider():

    def __init__(self, config: dict):
        self.config = config

    def create_provider(self, provider: str):

        if provider == VectorDBEnums.QDRANT.value:
            return QdrantProvider(
                db_path=BaseController().get_vectordb_path(
                    self.config.QDRANT_DB_NAME
                ),
                distance_method=self.config.QDRANT_DISTANCE_METHOD.value,
            )

        return None

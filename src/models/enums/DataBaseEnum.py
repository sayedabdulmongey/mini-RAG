from enum import Enum


class DataBaseEnum(Enum):
    '''
    This class is an Enum class that contains the names of the collections in the database.
    It has the following attributes:
    COLLECTION_PROJECT_NAME: This attribute contains the name of the collection that stores the project data
    COLLECTION_CHUNK_NAME: This attribute contains the name of the collection that stores the chunk data
    '''
    COLLECTION_PROJECT_NAME = 'projects'
    COLLECTION_CHUNK_NAME = 'chunks'
    COLLECTION_ASSETS_NAME = 'assets'

from enum import Enum


class VectorDBEnums(Enum):

    QDRANT = 'QDRANT'
    PGVECTOR = 'PGVECTOR'


class DistanceTypeEnums(Enum):

    COSINE = 'cosine'
    DOT = 'dot'


class PGVectorDistanceTypeEnums(Enum):

    COSINE = 'vector_cosine_ops'
    DOT = 'vector_l2_ops'


class PGVectorTableSchemaEnums(Enum):

    ID = 'id'
    VECTOR = 'vector'
    TEXT = 'text'
    CHUNK_ID = 'chunk_id'
    METADATA = 'metadata'
    _PREFIX = 'pgvector_'


class PGVectorIndexingEnums(Enum):

    HNSW = 'hnsw'
    IVFFLAT = 'ivfflat'

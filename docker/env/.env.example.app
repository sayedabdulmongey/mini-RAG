APP_NAME="mini-RAG"
APP_VERSION="0.1.0"

FILE_ALLOWED_TYPES=["text/plain", "application/pdf"]   # allowed types (txt, pdf)
FILE_ALLOWED_SIZE=100 #MB
FILE_DEFAULT_CHUNK=512000 #512KB



POSTGRES_USERNAME="postgres"
POSTGRES_PASSWORD="<your_postgres_password>"
POSTGRES_HOST="pgvector"
POSTGRES_PORT=5432
POSTGRES_DATABASE="minirag-postgres"


############################################## LLM CONFIG ##############################################

GENERATION_BACKEND="GOOGLE"
EMBEDDING_BACKEND="GOOGLE"

COHERE_API_KEY="<your_cohere_api_key>"

OPENAI_API_KEY="<your_openai_api_key>"
OPENAI_URL_BASE="https://openrouter.ai/api/v1"

GOOGLE_API_KEY="<your_google_api_key>"

GENERATION_MODEL_ID="gemini-2.5-pro"
EMBEDDING_MODEL_ID="text-embedding-004"
EMBEDDING_SIZE=768

DEFAULT_INPUT_MAX_CHARACTERS=1000
DEFAULT_MAX_NEW_TOKENS=1000
DEFAULT_TEMPERATURE=0.1


############################################## VectorDB CONFIG ##############################################

VECTOR_DB_BACKEND_LITERAL=["QDRANT", "PGVECTOR"]
VECTOR_DB_BACKEND="PGVECTOR"
VECTOR_DB_PATH="pgvectordb"  
VECTOR_DB_DISTANCE_METHOD="cosine"
VECTOR_DB_PG_INDEXING_THRESHOLD=1000

############################################## Templates CONFIG ##############################################

DEFAULT_LANGUAGE="en"
PRIMARY_LANGUAGE="ar"

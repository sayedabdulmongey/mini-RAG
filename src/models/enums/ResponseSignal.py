from enum import Enum


class ResponseSignal(Enum):

    '''
    This class is an Enum that contains the possible values for the response signals that can be sent to the client.
    Possible values are:
    - FILE_VALIDATED_SUCCESS: 'file_validate_successfully'
    - FILE_TYPE_NOT_SUPPORTED: 'file_type_not_supported'
    - FILE_SIZE_EXCEEDED: 'file_size_exceeded'
    - FILE_UPLOAD_SUCCESS: 'file_upload_success'
    - FILE_UPLOAD_FAILED: 'file_upload_failed'
    - PROCESS_FAILED: 'file_processing_failed'
    - PROCESS_SUCCESS: 'file_processing_success'
    - FILE_PROCESS_FAILED: 'no_file_found'
    - FILE_PROCESS_NOT_FOUND: 'no_file_found_with_this_id'
    - PROJECT_NOT_FOUND: 'project_not_found'
    - CHUNK_INSERTION_TO_VECTORDB_FAILED: 'chunk_insertion_to_vectordb_failed'
    - CHUNK_INSERTION_TO_VECTORDB_SUCCESS: 'chunk_insertion_to_vectordb_succeed'
    - GET_PROJECT_INFO_FAILED: 'get_project_info_failed'
    - GET_PROJECT_INFO_SUCCESS: 'get_project_info_succeed'
    - VECTORDB_SEARCH_ERROR: 'vectordb_search_error'
    - VECTORDB_SEARCH_SUCCESS: 'vectordb_search_success'
    - RAG_ANSWER_ERROR: 'rag_answer_error'
    - RAG_ANSWER_SUCCESS: 'rag_answer_success'
    '''

    FILE_VALIDATED_SUCCESS = "file_validate_successfully"
    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_UPLOAD_SUCCESS = "file_upload_success"
    FILE_UPLOAD_FAILED = "file_upload_failed"

    PROCESS_FAILED = 'file_processing_failed'
    PROCESS_SUCCESS = 'file_processing_success'

    FILE_PROCESS_FAILED = 'no_file_found'
    FILE_PROCESS_NOT_FOUND = 'no_file_found_with_this_id'

    PROJECT_NOT_FOUND = 'project_not_found'

    CHUNK_INSERTION_TO_VECTORDB_FAILED = 'chunk_insertion_to_vectordb_failed'
    CHUNK_INSERTION_TO_VECTORDB_SUCCESS = 'chunk_insertion_to_vectordb_succeed'

    GET_COLLECTION_INFO_FAILED = 'get_collection_info_failed'
    GET_COLLECTION_INFO_SUCCESS = 'get_collection_info_succeed'

    VECTORDB_SEARCH_ERROR = 'vectordb_search_error'
    VECTORDB_SEARCH_SUCCESS = 'vectordb_search_success'

    RAG_ANSWER_ERROR = 'rag_answer_error'
    RAG_ANSWER_SUCCESS = 'rag_answer_success'

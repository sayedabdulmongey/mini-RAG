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
    '''

    FILE_VALIDATED_SUCCESS = "file_validate_successfully"
    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_UPLOAD_SUCCESS = "file_upload_success"
    FILE_UPLOAD_FAILED = "file_upload_failed"

    PROCESS_FAILED = 'file_processing_failed'
    PROCESS_SUCCESS = 'file_processing_success'

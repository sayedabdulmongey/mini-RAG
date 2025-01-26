from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseSignal
import re
import os


class DataController(BaseController):
    '''
    This is the DataController class that will be used to handle all data related operations
    It inherits from the BaseController class
    It has the following methods:

    validate_uploaded_file: This method validates the uploaded file based on the file type and size

    generate_unique_filepath: This method generates a unique file path for the uploaded file

    clean_filename: This method cleans the filename by removing all special characters
    '''

    def __init__(self):

        super().__init__()
        self.size_convert = 1 << 20

    def validate_uploaded_file(self, file: UploadFile):
        '''
        This method validates the uploaded file based on the file type and size
        Allowed file types and size are defined in the app settings
        '''

        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value, file.content_type
        
        # file.size >> byte , file_allowed_size >> mega byte
        if file.size > self.app_settings.FILE_ALLOWED_SIZE*self.size_convert:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value, file.content_type
        
        return True, ResponseSignal.FILE_UPLOAD_SUCCESS.value, file.content_type

    def generate_unique_filepath(self, file: UploadFile, project_id: str):

        random_key = self.generate_random_string()

        project_control = ProjectController()
        project_dir = project_control.get_project_path(project_id)
        file_name = self.clean_filename(file.filename)
        file_path = os.path.join(
            project_dir,
            f"{random_key}_{file_name}"
        )

        while os.path.exists(file_path):
            random_key = self.generate_random_string()
            file_path = os.path.join(
                project_dir,
                f"{random_key}_{file.filename}"
            )
        return file_path, f'{random_key}_{file.filename}'

    def clean_filename(self, filename: str):
        '''
        This method cleans the filename by removing all special characters from the filename
        '''
        # remove all special characters
        cleaned_filename = re.sub(r'[^\w_.]', '', filename.strip())

        return cleaned_filename

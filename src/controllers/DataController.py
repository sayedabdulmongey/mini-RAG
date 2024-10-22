from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseSignal
import re
import os 
class DataController(BaseController):


    def __init__(self):

        super().__init__()
        self.size_convert = 1 << 20

    def validate_uploaded_file(self,file:UploadFile):
        response_signals = ResponseSignal
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False,response_signals.FILE_TYPE_NOT_SUPPORTED.value
        if file.size > self.app_settings.FILE_ALLOWED_SIZE*self.size_convert : # file.size >> byte , file_allowed_size >> mega byte
            return False,response_signals.FILE_SIZE_EXCEEDED.value
        return True,response_signals.FILE_UPLOAD_SUCCESS.value
    def generate_unique_filepath(self,file:UploadFile,project_id:str):

        random_key = self.generate_random_string()

        project_control = ProjectController()
        project_dir = project_control.get_project_path(project_id)
        file_name = self.clean_filename(file.filename)
        file_path=os.path.join(
            project_dir,
            f"{random_key}_{file_name}"
        )

        while os.path.exists(file_path):
            random_key = self.generate_random_string()
            file_path=os.path.join(
                project_dir,
                f"{random_key}_{file.filename}"
            )
        return file_path,f'{random_key}_{file.filename}'
    
    def clean_filename(self,filename:str):


        cleaned_filename = re.sub(r'[^\w_.]', '', filename.strip())

        return cleaned_filename

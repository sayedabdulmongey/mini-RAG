from .BaseController import BaseController
import os


class ProjectController(BaseController):

    '''
    This is the ProjectController class that will be used to handle all project related operations
    It inherits from the BaseController class
    It has the following methods:

    get_project_path: This method gets the project path based on the project id
    '''

    def __init__(self):
        super().__init__()

    def get_project_path(self, project_id: str):

        project_dir = os.path.join(
            self.file_dir,
            project_id
        )
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)

        return project_dir

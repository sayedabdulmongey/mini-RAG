from helpers import get_settings, Settings
import os
import random
import string


class BaseController:
    '''
    This is the base controller class that will be inherited by all other controllers
    In the constructor, it initializes the app_settings and the base_dir and file_dir attributes
    app_settings: This is the settings object that contains all the settings from the .env file
    base_dir: This is the base directory of the project 
    file_dir: This is the directory where the files will be stored

    generate_random_string: This method generates a random string of length max_len
    '''

    def __init__(self):
        self.app_settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        print(self.base_dir)
        self.file_dir = os.path.join(
            self.base_dir,
            'assets/files'
        )

    def generate_random_string(self, max_len: int = 15):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=max_len))

from helpers import get_settings,Settings
import os 
import random
import string
class BaseController:
    def __init__(self):
        self.app_settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        print(self.base_dir)
        self.file_dir = os.path.join(
            self.base_dir,
            'assets/files'
        )
    def generate_random_string(self,max_len:int=15):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=max_len))






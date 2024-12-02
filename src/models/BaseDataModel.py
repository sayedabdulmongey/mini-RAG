from helpers import get_settings


class BaseDataModel():

    '''
    BaseDataModel class is the parent class for all the data models in the application
    In this class, we have the db_client object which is the connection to the database, 
                           the app_settings object which contains the application settings
    '''

    def __init__(self, db_client: object):
        self.db_client = db_client
        self.app_settings = get_settings()

from .BaseDataModel import BaseDataModel
from .enums.DataBaseEnum import DataBaseEnum
from .db_schemas import Project


class ProjectModel(BaseDataModel):
    '''
    ProjectModel class is the data model for the projects collection in the database
    In this class, we have the following methods:
    - create_project: to insert a new project into the projects collection
    - get_project_or_create_one: to retrieve a project from the projects collection or create a new one if it doesn't exist
    - get_all_projects: to retrieve all the projects from the projects collection with pagination
    '''

    def __init__(self, db_client: object):
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]

    @classmethod
    async def create_instance(cls, db_client: object):
        '''
        I created this method because i want to call async method (init_collections) in the init but its not allowed to call async method in the init because its not awaitable
        So i created this method to call the init method and the async method also 
        '''
        instance = cls(db_client)
        await instance.init_collections()
        return instance

    async def init_collections(self):
        '''
        This method is used to initialize the collections in the database
        The Initialization includes creating the indexes for the collections for the first time only
        '''
        all_collections = await self.db_client.list_collection_names()
        indexes = Project.get_indexes()
        if DataBaseEnum.COLLECTION_PROJECT_NAME.value not in all_collections:
            for index in indexes:
                await self.collection.create_index(
                    index['key'],
                    name=index['name'],
                    unique=index['unique']
                )

    async def create_project(self, project: Project):
        '''
        Create a new project in the projects collection
        '''
        result = await self.collection.insert_one(project.dict(by_alias=True, exclude_unset=True))
        # by_alias=True: to use the alias name in the schema
        # exclude_unset=True: to exclude the fields that are not set in the schema which means the values that aren't provided in the project object will be equal to None
        # i do this because i solve problem with acces _id which is private attribute so i used alias to access it

        project._id = result.inserted_id

        return result

    async def get_project_or_create_one(self, project_id: str):

        records = await self.collection.find_one({
            'project_id': project_id
        })

        if records is None:
            # create new project

            project = Project(project_id=project_id)
            records = await self.create_project(project=project)

            return records

        return Project(**records)
        # Because the records is a dictionary, we need to convert it to a Project object

    async def get_all_projects(self, page: int = 1, page_size: int = 10):

        # get the total number of documents in the collection
        total_documents = self.collection.count_documents()

        # calculate the total number of pages

        total_pages = (total_documents+page_size -
                       1) // page_size  # Ceil Operation

        cursor = self.collection.find().skip((page-1)*page_size).limit(page_size)
        # documents = list(cursor) # this way is not recommended because it will load all the documents in the memory

        # More efficient way to get the documents by using the async for loop in the cursor
        projects = []
        async for documents in cursor:
            projects.append(
                Project(**documents)
            )

        return projects, total_pages

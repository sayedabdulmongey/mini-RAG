from .BaseDataModel import BaseDataModel
from .enums.DataBaseEnum import DataBaseEnum
from .db_schemas import Project

from sqlalchemy.future import select
from sqlalchemy import func


class ProjectModel(BaseDataModel):
    '''
    ProjectModel class is the data model for the projects collection in the database
    The class is responsible for all the operations related to the projects collection in the database
    The class inherits from the BaseDataModel class which is responsible for the database connection

    The class has the following methods:
    - create_instance: This method is used to create an instance of the ProjectModel class
    - create_project: This method is used to create a new project in the database
    - get_project_or_create_one: This method is used to get a project from the database by its id
    - get_all_projects: This method is used to get all the projects from the database
    '''

    def __init__(self, db_client: object):
        super().__init__(db_client)

    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)
        return instance

    async def create_project(self, project: Project):

        async with self.db_client() as session:
            async with session.begin():
                session.add(project)
            await session.commit()
            # This is to refresh the project object with the new values from the database
            await session.refresh(project)

        return project

    async def get_project_or_create_one(self, project_id: int):

        async with self.db_client() as session:
            async with session.begin():
                query = select(Project).where(Project.project_id == project_id)
                result = await session.execute(query)
                project = result.scalar_one_or_none()

                if project is None:
                    project_rec = Project(project_id=project_id)
                    project = await self.create_project(project=project_rec)

                return project

    async def get_all_projects(self, page: int = 1, page_size: int = 10):

        async with self.db_client() as session:
            async with session.begin():

                total_documents_query = select(func.count(Project.project_id))
                total_documents_result = await session.execute(total_documents_query)
                total_documents = total_documents_result.scalar_one()

                # calculate the total number of pages

                total_pages = (total_documents+page_size -1) // page_size  # Ceil Operation

                project_query = select(Project).offest(
                    (page-1)*page_size).limit(page_size)

                projects = await session.execute(project_query).scalars().all()

                return projects, total_pages

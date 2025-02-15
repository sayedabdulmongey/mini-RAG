from .BaseController import BaseController
from .ProjectController import ProjectController
import os
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# I used this one because its smart in splitting its split in appropriate positions like wait to close the brackets and so on ...

from models import ProcessEnum


class ProcessController(BaseController):

    '''
    This is the ProcessController class that will be used to handle all process related operations
    It inherits from the BaseController class
    It has the following methods:

    get_file_extension: This method gets the file extension of the file

    get_file_loader: This method gets the file loader based on the file extension

    get_file_content: This method gets the content of the file

    get_file_chunks: This method gets the chunks of the file content

    get_file_name_from_metadata: This method gets the file name from the metadata

    '''

    def __init__(self, project_id: int):
        super().__init__()

        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)

    def get_file_extension(self, file_id: str):
        return os.path.splitext(file_id)[-1]

    def get_file_name_from_metadata(self, metadata: dict):
        '''
        This function extracts the file name from the metadata and from the source key
        ex: source: 'home/user/Xvxj2DnWk6fbfKV_file.txt' => file.txt
        '''
        return os.path.basename(metadata['source']).split('_', 1)[-1]

    def get_file_loader(self, file_id: str):

        self.file_path = os.path.join(
            self.project_path,
            file_id
        )

        if not os.path.exists(self.file_path):
            return None

        file_extension = self.get_file_extension(file_id=file_id)

        if file_extension == ProcessEnum.TXT.value:
            return TextLoader(
                file_path=self.file_path,
                encoding='UTF-8'
            )
        elif file_extension == ProcessEnum.PDF.value:
            return PyMuPDFLoader(
                file_path=self.file_path
            )

        return None

    def get_file_content(self, file_id: str):

        loader = self.get_file_loader(file_id=file_id)

        if loader:
            return loader.load()

        return None

    def get_file_chunks(self, file_content: list,
                        chunk_size: int = 100, overlap_len: int = 10):

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_len,
            length_function=len,
        )

        file_content_texts = [
            rec.page_content
            for rec in file_content
        ]

        file_content_metadata = [
            rec.metadata
            for rec in file_content
        ]

        chunks = text_splitter.create_documents(
            texts=file_content_texts,
            metadatas=file_content_metadata,
        )

        return chunks

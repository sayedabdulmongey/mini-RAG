from .BaseController import BaseController
from .ProjectController import ProjectController
import os 
from langchain_community.document_loaders import TextLoader,PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# i used this one because its smart in splitting its split in appropriate positions like wait to close the brackets and so on ...

from models import ProcessEnum


class ProcessController(BaseController):

    def __init__(self,project_id:str):

        self.project_id = project_id

        self.project_path = ProjectController().get_project_path(project_id=project_id)


    def get_file_extension(self,file_id:str):
        return os.path.splitext(file_id)[-1]


    def get_file_loader(self,file_id:str):

        self.file_path = os.path.join(
            self.project_path,
            file_id
        )

        file_extension = self.get_file_extension(file_id=file_id)

        if file_extension==ProcessEnum.TXT.value:
            return TextLoader(
                file_path=self.file_path,
                encoding='UTF-8'
            )
        elif file_extension == ProcessEnum.PDF.value:
            return PyMuPDFLoader(
                file_path=self.file_path
            )
        
        return None
        
    def get_file_content(self,file_id:str):

        loader = self.get_file_loader(file_id=file_id)
        return loader.load()
    
    def get_file_chunks(self,file_content:list,file_id:str,
                        chunk_size:int=100,overlap_len:int=10):
        
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
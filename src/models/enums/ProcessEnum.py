from enum import Enum


class ProcessEnum(Enum):
    '''
    This class is an Enum that contains the possible values for the file types that can be processed.
    Possible values are:
    - PDF: '.pdf'
    - TXT: '.txt'
    '''
    PDF = '.pdf'
    TXT = '.txt'

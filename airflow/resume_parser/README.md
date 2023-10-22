# **Resume Parser Package**
![Resume Parser Workflow](data\ResumeParser_workflow.png)

## **Introduction**
This package include Python scripts to parse Resume from PDF into JSON format and powered by LangChain


## **Source Structure**
~~~~~~~
resumeparser
    |-- __init__.py         : Module to contain instance that can directly imported (ResumeParser,...)
    |-- src
        |-- config.py       : Module contain configurations for resume Parser and LangChain APIs
        |-- resume_parser.py: Module define resume parser object
        |-- utils.py        : Module contains all helper functions.
    |-- data
        |-- resume          : Folder contain all resume as PDF
        |-- parsed_resume   : Folder contain all resume after parsed to JSON format
    |-- resume_parser.ipynb : Notebook to implement resume parser
    |-- README.md
~~~~~~~


## **Usage**
- All configurations about Resume Parser/LangChain client/Prompt... can be modified in **src/config.py**
- Checkout this script to run ResumeParser (or reference from **resume_parser.ipynb**)
~~~~~~~
from resume_parser import RESUMEPARSER

# Parse single resume
parsed_resume =  RESUMEPARSER.parse_resume(<resume_path>)
~~~~~~~

Or parse multiple resumes in a folder or azure storage container
~~~~~~~
from resume_parser import RESUMEPARSER
from src.utils import apply_function_multithreaded

# Multiprocessing function with threading
# Note that file_to_parse must be iterable object with this format: [(arg_1, arg_2,...), ...]
parsed_resumes = apply_function_multithreaded(RESUMEPARSER.parse_resume, (files_to_parse))
~~~~~~~


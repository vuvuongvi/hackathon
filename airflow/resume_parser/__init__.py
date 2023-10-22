"""
This module initial object that related to resume parser and can directly be imported
"""


# Import dependencies
import warnings
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
warnings.filterwarnings("ignore")

from resume_parser.src.config import AzureOpenAIConfiguration as API_CFG
from resume_parser.src.config import ResumeParserConfiguration as PARSER_CFG
from resume_parser.src.resume_parser import ResumeParser

# Initial Resume Parser object
RESUMEPARSER = ResumeParser(env=PARSER_CFG.enviroment,
                            storage_path_or_container=PARSER_CFG.storage_path_or_container,
                            prompt=PARSER_CFG.prompt,
                            api_base_url=API_CFG.api_base_url,
                            api_version=API_CFG.api_version,
                            api_key=API_CFG.api_key,
                            api_type=API_CFG.api_type,
                            deployment_name=API_CFG.development_name)

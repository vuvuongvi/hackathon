"""
This module contain configurations for resume_parser package
"""
import os
# The code `from dotenv import load_dotenv` and `load_dotenv()` are used to load environment variables
# from a .env file into the current environment.
from dotenv import load_dotenv
load_dotenv()

class AzureOpenAIConfiguration:
    """
    Configuration parameters for AzureOpenAI Client
    """

    api_base_url = os.environ.get("AZURE_OPEN_AI_URL")
    api_key = os.environ.get("AZURE_OPEN_AI_KEY")
    api_version = "2023-05-15"
    api_type = 'azure'
    development_name = os.environ.get("AZURE_OPEN_AI_DEV_NAME")

class ResumeParserConfiguration:
    """
    Configuration for ResumeParser (prompt template for chat model,...)
    """
    # Enviroment param to configure which place to store result (azure-cloud OR local)
    enviroment = 'local'

    # Absolute path to folder that store results OR Azure Storage Container
    storage_path_or_container = 'parsed-resume'

    # Prompt template for chat model
    prompt = """
        We have a text extracted from Q/A for our internal process in a TEXT format. We need to do the following:

        1. Extract entities from the text, TEXT file contains multiple paragraphs separated by double newline. Each paragraph have a pair Q/A.
        2. Translate these entities into both English and Japanese => each paragraph will have threes version of languages (original, English and Japanese).
        3. Create three JSON objects for each paragraph for three languages repectively.
        4. Put all these JSON objects into a list.
        It's important to note that if we have 2 paragraphs in the file, the result will include 6 JSON objects in the list:
            - first layer is list
            - second layer is three JSON objects respective three languages, each JSON is:
                + question -> str: question of user in each paragraph
                + answer -> str: answer of question of user in the same paragraph
        Please ensure that the information is accurately extracted and formatted. If any section is too lengthy, feel free to summarize it so that it fits within the JSON structure.
    """
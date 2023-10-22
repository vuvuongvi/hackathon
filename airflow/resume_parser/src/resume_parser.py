"""
Resume Parsing Module

This module provides functionality for parsing resumes from PDF files and converting them
into structured JSON data. It leverages external libraries for PDF processing and utilizes
ChatGPT for entity extraction.
"""

import os
import ast
import langchain
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.cache import InMemoryCache

from resume_parser.src.utils import (
    extract_pdf_to_text, read_text_from_storage,
    initial_azure_storage_blob_client
)

from ultil.init_azure_storage import (
    storage_conn_str, 
    storage_container_name_raw
)

class ResumeParser:
    """
    A utility for parsing resumes from PDF files, extracting text content,
    and utilizing ChatGPT model for entity extraction and structuring.
    """
    # Configurations for azure storage blob
    env: str
    storage_path_or_container: str

    # Configurations for LangChain ChatOpenAI API
    api_base_url: str
    api_version: str
    api_key: str
    api_type: str
    deployment_name: str
    prompt: str

    # Attributes of ResumeParser
    extracted_resume: str
    raw_response: str
    parsed_resume: object
    list_parsed_resumes: list

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        # Initial Azure ChatOpenAI Client
        self.initial_chat_model_client()

        # Initial caching layer for chat model
        self.initial_caching_layer()

        # Initial the prompt template for chat model
        self.initial_prompt_template()

    def initial_chat_model_client(self) -> AzureChatOpenAI:
        """
        Initial the Azure ChatOpenAI Client
        """
        self.chat_model = AzureChatOpenAI(
            openai_api_base=self.api_base_url,
            openai_api_version=self.api_version,
            openai_api_key=self.api_key,
            openai_api_type=self.api_type,
            deployment_name=self.deployment_name,
        )

    def initial_caching_layer(self) -> InMemoryCache:
        """
        Initial the caching layer for chat model. This is useful for two reasons:
        1. It can save you money by reducing the number of API calls you make to the LLM provider
        (if you're often requesting the same completion multiple times)
        2. It can speed up your application by reducing the number of API calls you make
        to the LLM provider.
        """
        langchain.llm_cache = InMemoryCache()

    def initial_prompt_template(self) -> PromptTemplate:
        """
        Initial the prompt template for chat model
        """
        self.prompt_template = PromptTemplate.from_template(
            self.prompt + "\n {resume}?")

    def format_input(self, extracted_resume: str = None) -> str:
        """
        Format input message for chat model with prompt template
        :param extracted_resume: plain text content extracted from PDF resume
        :return: formatted input with prompt template
        """
        if not extracted_resume:
            extracted_resume = self.extracted_resume

        try:
            formatted_input = self.prompt_template.format(
                resume=extracted_resume)
        except:
            # pylint: disable=W0707
            # pylint: disable=W0719
            formatted_input = None
            raise Exception("Fail to format input with prompt template")

        return formatted_input

    def format_output(self, response: str = None) -> object:
        """
        Parse response of chat model from string into object
        :param response: raw response returned by chat model
        :return: object converted from response as string
        """
        if not response:
            response = self.raw_response

        try:
            formatted_output = ast.literal_eval(response)
        except:
            # pylint: disable=W0707
            # pylint: disable=W0719
            formatted_output = None
            raise Exception("Fail to format response from chat model")

        return formatted_output

    def parse_resume(self, file_object: object, blob_name: str=None) -> object:
        """
        Extract entities that have been predefined from PDF file
        :param file_object: A File object or could also be a string representing path to PDF file.
        :param blob_name: blob name (only required if env is 'azure-cloud')
        :return: parsed resume as JSON object
        """
        if self.env == 'azure-cloud':
            file_name = blob_name
        else:
            file_name_with_extension = os.path.basename(file_object)
            file_name = os.path.splitext(file_name_with_extension)[0]

        try:
            # Extract content in PDF file into text
            # self.extracted_resume = extract_pdf_to_text(file_object) # extrat from PDF
            self.extracted_resume = read_text_from_storage(file_object, storage_conn_str, storage_container_name_raw) # extract from .TXT

            # Format input message with prompt template
            formatted_input = self.format_input()

            # Get response from chat model
            # TODO: retry
            self.raw_response = self.chat_model.predict(formatted_input)

            # Format response into JSON object (or dictionary)
            self.parsed_resume = self.format_output()

            print(f"Parsing resume {file_name + '...':<30} ✓")

        except Exception as exception:# pylint: disable=W0718
            self.parsed_resume = {}
            print(f"Parsing resume {file_name + '...':<30} X --> {exception}")

        return self.parsed_resume

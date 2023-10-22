"""
This module contain helper functions for resume_parser package
"""
import json
import PyPDF2
import yaml
from azure.storage.blob import BlobServiceClient, BlobClient
from concurrent.futures import ThreadPoolExecutor

def extract_pdf_to_text(file_object: str) -> str:
    """
    Extract content in PDF file into text
    :param file_object: A File object or could also be a string representing a path to a PDF file.
    :return : text content extracted from PDF file
    """
    try:
        reader = PyPDF2.PdfReader(file_object)
        num_pages = len(reader.pages)
        text = ""

        for page in range(num_pages):
            current_page = reader.pages[page]
            text += current_page.extract_text()
    except:
            # pylint: disable=W0707
            # pylint: disable=W0719
        text = ""
        raise Exception("Fail to extract text from PDF file")

    return text

def read_text_from_storage(file_object: str, storage_conn_str: str, storage_container_name: str) -> str:
    """
    Extract content in .txt file 
    :param file_object: A File object or could also be a string representing a path to a .txt file.
    :return : text content extracted
    """
    blob_client = BlobClient.from_connection_string(conn_str=storage_conn_str, 
                                                    container_name=storage_container_name, 
                                                    blob_name=file_object)
    blob_data = blob_client.download_blob()
    blob_content = blob_data.readall()
    text_content = blob_content.decode('utf-8')

    return text_content

def save_json_to_storage(data: object, file_object: str, storage_conn_str: str, storage_container_name: str):
    """
    Save data as json object/dictionary to JSON file in storage
    :param data: input data that need to saved as JSON file
    :param file_path: path to save JSON file
    """
    blob_client = BlobClient.from_connection_string(conn_str=storage_conn_str, 
                                                    container_name=storage_container_name, 
                                                    blob_name=file_object)
    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    blob_client.upload_blob(json_data, overwrite=True)

def save_yaml(data: object, file_path: str):
    """
    Save data as json object/dictionary to YAML file
    :param data: input data that need to saved as YAML file
    :param file_path: path to save YAML file
    """
    # Convert JSON to YAML and save to a file
    with open(file_path, 'w', encoding='utf-8') as file:
        yaml.dump(data, file)

def save_json(data: object, file_path: str):
    """
    Save data as json object/dictionary to JSON file
    :param data: input data that need to saved as JSON file
    :param file_path: path to save JSON file
    """
    # Save data into JSON file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file)

def initial_azure_storage_blob_client(connection_string: str) -> BlobServiceClient:
    """
    Initial Azure Storage Blob Client
    :param connection_string: string provide connection key to Azure Storage Blob Client
    :return: Azure Storage Blob Client
    """
    # Initial blob service client
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    return blob_service_client

def upload_to_azure_blob(blob_service_client: BlobServiceClient,
                         container_name: str,
                         blob_name: str,
                         data: object):
    """
    Store data into Azure Storage Blob
    :param blob_service_client: Azure Storage Blob Client
    :param container_name: Azure Storage Container name
    :param blob_name: Azure Storage Blob name
    :param data: input data that need to upload to Azure Storage Blob
    """
    # Get container client
    container_client = blob_service_client.get_container_client(container_name)

    # Get blob client
    blob_client = container_client.get_blob_client(blob_name)

    # Upload data into azure blob storage
    blob_client.upload_blob(str(data), overwrite=True)

def retrieve_from_azure_blob(blob_service_client: BlobServiceClient,
                             container_name: str,
                             blob_name: str) -> object:
    """
    Get data from Azure Storage Blob
    :param blob_service_client: Azure Storage Blob Client
    :param container_name: Azure Storage Container name
    :param blob_name: Azure Storage Blob name
    :return: content read from Azure Storage Blob
    """
    # Get container client
    container_client = blob_service_client.get_container_client(container_name)

    # Get blob client
    blob_client = container_client.get_blob_client(blob_name)

    # Download blob
    content = blob_client.download_blob().readall()

    return content

def apply_function_multithreaded(func: callable, arg_tuples: list) -> list:
    """
    Apply a function to a list of argument tuples using threading.
    :param func: The function to apply.
    :param arg_tuples: List of tuples where each contains the arguments for a single function call.
    :return: List of results from applying the function to the arguments.
    """
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(func, *zip(*arg_tuples)))

    return results

from __future__ import annotations
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow import DAG, Dataset
from datetime import timedelta, datetime
import os
from llama_index import download_loader, GPTMilvusIndex
from azure.storage.blob import BlobClient
import pendulum

import sys
from pathlib import Path
parent = Path(os.getcwd())
sys.path.append(str(parent.parent))
from resume_parser import RESUMEPARSER
from resume_parser.src.utils import (
    save_json_to_storage
)
from ultil.init_azure_storage import (
    storage_conn_str, storage_container_name_transform
)

HOST = "localhost"
PORT = "19530"
AZURE_CONNECTION_STRING = os.environ.get('AZURE_CONNECTION_STRING')
AZURE_CONTAINER_NAME = os.environ.get('AZURE_CONTAINER_NAME')


def get_azure_storage_and_push_xcom(**kwargs):
    blob = BlobClient.from_connection_string(conn_str="", container_name="rawdata")
    blob_data = blob.download_blob()
    print(blob_data)
    kwargs['ti'].xcom_push(key='questionanswer', value=blob_data)

def transform_to_json(raw_text_file: str, transform_json_file: str, 
                      storage_container_name_transform: str, storage_conn_str: str):
    """
    Transform data from raw text to json and save to storage. This is a wrapper for RESUMEPARSER. parse_resume and flatten to correct format
    
    @param raw_text_file - Path to raw text file
    @param transform_json_file - Path to transform json file
    @param storage_container_name_transform - Name of storage container to be used for transformation. Default is None. \
        If you want to use different storage container name you can specify it here.
    @param storage_conn_str - connection string to storage. Default is None
    """
    # parse text to json
    print(f"PROCESSING PARSER DATA....")
    parsed_resume =  RESUMEPARSER.parse_resume(file_object=raw_text_file)

    # flatten json to correct format
    flattened_data = []
    for item in parsed_resume:
        values = [value for value in item.values()]
        flattened_data.extend(values)

    # write result data to storage
    save_json_to_storage(data=flattened_data, 
                     file_object=transform_json_file,
                     storage_conn_str=storage_conn_str,
                     storage_container_name=storage_container_name_transform)
    print(f"tranform successful from {raw_text_file} to {transform_json_file}!")

def import_milvus():
    blob = BlobClient.from_connection_string(conn_str=AZURE_CONNECTION_STRING, container_name=AZURE_CONTAINER_NAME, blob_name="Q_A_for_admin.txt")
    blob_data = blob.download_blob()

    JsonDataReader = download_loader("JsonDataReader")
    loader = JsonDataReader()
    documents = loader.load_data(blob_data)
    # Put JSON into Milvus
    GPTMilvusIndex.from_documents(documents, host=HOST, port=PORT, overwrite=True)

with DAG(
    dag_id="Extract_dataset",
    schedule_interval='@dataset',
    catchup=False,
    tags=["extract", "dataset-scheduled"],
) as extract_dag:
    PythonOperator(
        task_id = "extract_dataset",
        provide_context=True,
        python_callable=get_azure_storage,
        dag=extract_dag,
    )

with DAG(
    dag_id="Transform_dataset",
    schedule_interval='@dataset',
    catchup=False,
    tags=["transform", "data-scheduled"]
) as transform_dag:
    PythonOperator(
        task_id = "transform_dataset",
        provide_context=True,
        python_callable=transform_to_json,
        dag=transform_dag
    )

with DAG(
    dag_id="Import_dataset_vectordb",
    schedule_interval='@dataset',
    catchup=False,
    tags=["import", "data-scheduled"]
) as import_dataset:
    PythonOperator(
        task_id = "import_dataset",
        provide_context=True,
        python_callable=import_milvus,
        dag=transform_dag
    )

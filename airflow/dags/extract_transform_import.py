from __future__ import annotations
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow import DAG, Dataset
from datetime import timedelta, datetime
from os import environ
from llama_index import download_loader, GPTMilvusIndex
from azure.storage.blob import BlobClient
import pendulum


HOST = "localhost"
PORT = "19530"


def get_azure_storage():
    blob = BlobClient.from_connection_string(conn_str="", container_name="rawdata")
    blob_data = blob.download_blob()
    


def transform_to_json():
    return 'transform to json'

def import_milvus():
    blob = BlobClient.from_connection_string(conn_str="", container_name="mycontainer", blob_name="my_blob")
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

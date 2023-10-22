from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow import DAG, Dataset
from datetime import timedelta, datetime
import os
from llama_index import download_loader, VectorStoreIndex
from azure.storage.blob import BlobClient
import pendulum
import json
from dotenv import load_dotenv
from pymilvus import utility, connections, Collection

load_dotenv()

HOST = "localhost"
PORT = "19530"
AZURE_CONNECTION_STRING = os.getenv('AZURE_CONNECTION_STRING')
AZURE_CONTAINER_NAME = os.getenv('AZURE_CONTAINER_NAME')


def get_azure_storage_and_push_xcom(**kwargs):
    blob = BlobClient.from_connection_string(conn_str="", container_name="rawdata")
    blob_data = blob.download_blob()
    print(blob_data)
    kwargs['ti'].xcom_push(key='questionanswer', value=blob_data)    
    


def transform_to_json():
    return 'transform to json'


def create_connection():
    print(f"\nCreate connection...")
    connections.connect(host=HOST, port=PORT)
    print(f"\nList connections:")
    print(connections.list_connections())

def insert_milvus(json_data):
    collection = Collection("qa")
    mr = collection.insert(json_data)
    print(mr, flush=True)

def import_milvus(**kwargs):
    blob = BlobClient.from_connection_string(conn_str=AZURE_CONNECTION_STRING, container_name=AZURE_CONTAINER_NAME, blob_name="transform_data.json")
    blob_data = blob.download_blob()
    fileReader = json.loads(blob_data.readall())
    vectordb_connect = create_connection()
    insert_json_to_milvus = insert_milvus(fileReader)

    # JsonDataReader = download_loader("JsonDataReader")
    # loader = JsonDataReader()
    # documents = loader.load_data(fileReader)
    # # Put JSON into Milvus
    # VectorStoreIndex.from_documents(documents, host=HOST, port=PORT, overwrite=True)

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


import_milvus()
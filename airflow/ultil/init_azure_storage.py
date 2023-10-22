from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
from azure.storage.blob.aio import BlobClient
import os
# The code `from dotenv import load_dotenv` and `load_dotenv()` are used to load environment variables
# from a .env file into the current environment.
from dotenv import load_dotenv
load_dotenv()

storage_conn_str = os.environ.get('STORAGE_CONN_STRING')
storage_account_name = os.environ.get("STORAGE_ACCOUNT_NAME")
storage_container_name_raw = os.environ.get('STORAGE_CONTAINER_NAME_RAW')
storage_container_name_transform = os.environ.get('STORAGE_CONTAINER_NAME_TRANSFORM')


token_credential = DefaultAzureCredential()

service = BlobServiceClient(
    account_url=f"https://{storage_account_name}.blob.core.windows.net/", 
    credential=token_credential
)
# blob = BlobClient.from_connection_string(conn_str="", container_nam="mycontainer", blob_name="my_blob")

# with open("./BlockDestination.txt", "wb") as my_blob:
#     stream = await blob.download_blob()
#     data = await stream.readall()
#     my_blob.write(data)

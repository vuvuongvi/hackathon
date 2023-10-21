from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
from azure.storage.blob.aio import BlobClient


token_credential = DefaultAzureCredential()

service = BlobServiceClient(
    account_url="https://<my-storage-account-name>.blob.core.windows.net/", 
    credential=token_credential
)
blob = BlobClient.from_connection_string(conn_str="", container_nam="mycontainer", blob_name="my_blob")

with open("./BlockDestination.txt", "wb") as my_blob
    stream = await blob.download_blob()
    data = await stream.readall()
    my_blob.write(data)
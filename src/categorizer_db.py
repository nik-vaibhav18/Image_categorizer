from azure.storage.blob import BlobServiceClient, ContentSettings
from azure.cosmos import CosmosClient, PartitionKey
from categorizer_func import generate_text
from uuid import uuid4
import os

COSMOS_KEY=os.getenv("COSMOS_KEY")
COSMOS_ENDPOINT=os.getenv("COSMOS_ENDPOINT")
COSMOS_DATABASE_NAME="nikhilcosmos_repo"
COSMOS_CONTAINER_NAME="cosmos_container"
BLOB_CONNECTION_STRING=os.getenv("BLOB_CONNECTION_STRING")
BLOB_CONTAINER_NAME="nikhilstore"



from azure.storage.blob import BlobServiceClient, ContentSettings
from azure.cosmos import CosmosClient, PartitionKey
from src.categorizer_func import generate_text
from uuid import uuid4
import os
from dotenv import load_dotenv
load_dotenv()

COSMOS_KEY=os.getenv("COSMOS_KEY")
COSMOS_ENDPOINT=os.getenv("COSMOS_ENDPOINT")
COSMOS_DATABASE_NAME="nikhilcosmos_repo"
COSMOS_CONTAINER_NAME="cosmos_container"
BLOB_CONNECTION_STRING=os.getenv("BLOB_CONNECTION_STRING")
BLOB_CONTAINER_NAME="nikhilstore"

blob_service_client=BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)

def upload_to_blob(image_path):
    blob_client = blob_service_client.get_blob_client(container=BLOB_CONTAINER_NAME, blob=os.path.basename(image_path))
    with open(image_path, "rb") as data:
        content_settings = ContentSettings(content_type="image/jpeg")
        container_client =blob_service_client.get_container_client(BLOB_CONTAINER_NAME)
        #container_client.create_container()
        blob_client.upload_blob(data, overwrite=True, content_settings=content_settings)
    return blob_client.url

cosmos_client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)


def initialize_cosmos():
    database = cosmos_client.create_database_if_not_exists(COSMOS_DATABASE_NAME)
    container = database.create_container_if_not_exists(
        id=COSMOS_CONTAINER_NAME,
        partition_key=PartitionKey(path="/image_id")
    )
    return container


def insert_metadata_to_cosmos(container, image_id, blob_url, gpt_response):
    item = {
        "id": image_id,  
        "image_id": image_id,
        "blob_url": blob_url,
        "gpt_response": gpt_response
    }
    container.upsert_item(item)


def search_cosmos_nested_field(field_path, field_value):
    """
    Query Cosmos DB for rows where a specific nested field contains the given value.
    
    Args:
    - field_path: The path to the nested field (e.g., 'gpt_response.seasonal_evergreen').
    - field_value: The value to search for (e.g., 'Mother\'s Day').

    Returns:
    - List of matching rows.
    """
    database = cosmos_client.get_database_client(COSMOS_DATABASE_NAME)
    container = database.get_container_client(COSMOS_CONTAINER_NAME)

    # Query to match a value inside a nested field
    query = f"""
    SELECT * FROM c
    WHERE ARRAY_CONTAINS(c.{field_path}, @field_value)
    """
    parameters = [{"name": "@field_value", "value": field_value}]

    results = list(container.query_items(query=query, parameters=parameters, enable_cross_partition_query=True))
    return results


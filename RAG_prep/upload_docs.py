from azure.cosmos import CosmosClient
import json
import os
from dotenv import load_dotenv


load_dotenv()

# Retrieve Cosmos DB connection details from environment variables
endpoint = os.getenv('COSMOS_ENDPOINT')
key = os.getenv('COSMOS_KEY')
database_name = os.getenv('COSMOS_DATABASE_NAME')
container_name = os.getenv('COSMOS_CONTAINER_NAME')

client = CosmosClient(endpoint, key)

database = client.get_database_client(database_name)
container = database.get_container_client(container_name)


def upload_data(json_file_path):
    """
    Uploads data from a JSON file to a specified Azure Cosmos DB container.

    Args:
        json_file_path (str): The file path of the JSON file containing the documents to be uploaded.
    """
    with open(json_file_path, 'r', encoding='utf-8') as file:
        documents = json.load(file)

        for doc in documents:
            try:
                container.upsert_item(doc)
                print(f"Document with id {doc['id']} inserted successfully.")
            except Exception as e:
                print(f"Failed to insert document {doc['id']}: {str(e)}")


script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative path to the JSON file
json_file_name = "all_documents.json"
json_file_path = os.path.join(script_dir, json_file_name)

if __name__ == '__main__':
    upload_data(json_file_path)

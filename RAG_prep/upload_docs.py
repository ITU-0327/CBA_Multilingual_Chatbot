from azure.cosmos import CosmosClient
import json
import os
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv('COSMOS_ENDPOINT')
key = os.getenv('COSMOS_KEY')
database_name = os.getenv('COSMOS_DATABASE_NAME')
container_name = os.getenv('COSMOS_CONTAINER_NAME')

client = CosmosClient(endpoint, key)
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)


def upload_data(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        documents = json.load(file)
        for doc in documents:
            try:
                container.upsert_item(doc)
                print(f"Document with id {doc['id']} inserted successfully.")
            except Exception as e:
                print(f"Failed to insert document {doc['id']}: {str(e)}")

json_file_path = 'c:/Users/itung/OneDrive/桌面/MIG-MON3075/CBA_Multilingual_Chatbot/RAG/all_documents.json'
upload_data(json_file_path)

from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient
from azure.search.documents import SearchClient
from azure.search.documents.indexes.models import (
    ComplexField,
    CorsOptions,
    SearchIndex,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    SearchIndexer,
)
import os


service_name = os.getenv('SERVICE_NAME')
admin_key = os.getenv('ADMIN_KEY')
index_name = os.getenv('INDEX_NAME')

# Setup the endpoint URL for the Azure Search service
endpoint = f"https://{service_name}.search.windows.net/"

# Initialize clients for managing indexes and searching
admin_client = SearchIndexClient(endpoint=endpoint,
                                  index_name=index_name,
                                  credential=AzureKeyCredential(admin_key))
search_client = SearchClient(endpoint=endpoint,
                             index_name=index_name,
                             credential=AzureKeyCredential(admin_key))

# Try to delete an existing index if it exists
try:
    admin_client.delete_index(index_name)
    print(f'Index {index_name} deleted')
except Exception as ex:
    print(ex)

# Define the fields for the search index
fields = [
    SimpleField(name="id", type=SearchFieldDataType.String, key=True),
    SearchableField(name="url", type=SearchFieldDataType.String, sortable=True),
    SearchableField(name="title", type=SearchFieldDataType.String, sortable=True),
    SearchableField(name="content", type=SearchFieldDataType.String, analyzer_name="en.lucene"),
    ComplexField(name="metadata", fields=[
        SimpleField(name="scrapedDate", type=SearchFieldDataType.DateTimeOffset, sortable=True),
        SearchableField(name="keywords", collection=True, type=SearchFieldDataType.String, facetable=True, filterable=True),
        SearchableField(name="description", type=SearchFieldDataType.String),
    ]),
    ComplexField(name="sections", collection=True, fields=[
        SearchableField(name="header", type=SearchFieldDataType.String),
        SearchableField(name="text", type=SearchFieldDataType.String),
    ]),
]

# CORS options for the index
cors_options = CorsOptions(allowed_origins=["*"], max_age_in_seconds=60)
scoring_profiles = []

# Create a new index with the defined fields
index = SearchIndex(
    name=index_name,
    fields=fields,
    scoring_profiles=scoring_profiles,
    cors_options=cors_options
)

# Try to create the new index
try:
    result = admin_client.create_index(index)
    print(f'Index {result.name} created.')
except Exception as ex:
    print(ex)

# Initialize the SearchIndexerClient
search_indexer_client = SearchIndexerClient(endpoint, AzureKeyCredential(admin_key))

# Configuration for the indexer
indexer_name = "cosmosdb-indexer"

# Create a SearchIndexer object
indexer = SearchIndexer(
    name=indexer_name,
    data_source_name="cba-support-docs",
    target_index_name=index_name
)

# Try to delete an existing indexer before creating a new one
try:
    search_indexer_client.delete_indexer(indexer_name)
    print("Existing indexer deleted.")
except Exception as e:
    print(f"Could not delete the existing indexer: {e}")

# Try to create the new indexer
try:
    search_indexer_client.create_indexer(indexer)
    print("Indexer created or updated.")
except Exception as e:
    print(f"Could not create indexer: {e}")

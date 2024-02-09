from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient 
from azure.search.documents import SearchClient
from azure.search.documents.indexes.models import (
    ComplexField,
    CorsOptions,
    SearchIndex,
    ScoringProfile,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    SearchIndexer,
    FieldMapping, 
    IndexingParameters
)
import os


service_name = os.getenv('SERVICE_NAME')
admin_key = os.getenv('ADMIN_KEY')
index_name = os.getenv('INDEX_NAME')

endpoint = f"https://{service_name}.search.windows.net/"
admin_client = SearchIndexClient(endpoint=endpoint,
                                  index_name=index_name,
                                  credential=AzureKeyCredential(admin_key))
search_client = SearchClient(endpoint=endpoint,
                             index_name=index_name,
                             credential=AzureKeyCredential(admin_key))

try:
    result = admin_client.delete_index(index_name)
    print ('Index', index_name, 'Deleted')
except Exception as ex:
    print (ex)


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

cors_options = CorsOptions(allowed_origins=["*"], max_age_in_seconds=60)
scoring_profiles = []

index = SearchIndex(
    name=index_name,
    fields=fields,
    scoring_profiles=scoring_profiles,
    cors_options=cors_options
)

try:
    result = admin_client.create_index(index)
    print(f'Index {result.name} created.')
except Exception as ex:
    print(ex)


search_indexer_client = SearchIndexerClient(endpoint, AzureKeyCredential(admin_key))

data_source_name = "cba-support-docs"
skillset_name = "cosmosdb-skillset"
target_index_name = "cosmosdb-index"
indexer_name = "cosmosdb-indexer"

indexer = SearchIndexer(
    name="cosmosdb-indexer",
    data_source_name="cba-support-docs",
    target_index_name=index_name,
    schedule=None,
)

try:
    search_indexer_client.delete_indexer(indexer_name)
    print("Existing indexer deleted.")
except Exception as e:
    print(f"Could not delete the existing indexer: {e}")

try:
    search_indexer_client.create_indexer(indexer)
    print("Indexer created or updated.")
except Exception as e:
    print(f"Could not create indexer: {e}")

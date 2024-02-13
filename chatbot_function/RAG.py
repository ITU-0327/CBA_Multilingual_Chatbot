from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
import os

from .openai_service import generate_openai_response
from .utils import get_sources_content, get_secret


service_name = os.environ["SERVICE_NAME"]
admin_key = get_secret('admin-key')  # Retrieve the admin key securely from Azure Key Vault. or 
index_name = os.environ["INDEX_NAME"]

# Template for prompting OpenAI to generate a search query based on a user's input.
query_prompt_template = """Below is a history of the conversation so far, and a new question asked by the user that needs to be answered by searching in a knowledge.
You have access to Azure AI Search index with 100's of documents.
Generate a search query based on the conversation and the new question.
Do not include cited source filenames and document names e.g info.txt or doc.pdf in the search query terms.
Do not include any text inside [] or <<>> in the search query terms.
Do not include any special characters like '+'.
If the question is not in English, translate the question to English before generating the search query.
If you cannot generate a search query, return just the number 0.
"""

# Configure the endpoint for the Azure Search Service.
endpoint = f"https://{service_name}.search.windows.net/"

search_client = SearchClient(endpoint=endpoint,
                             index_name=index_name,
                             credential=AzureKeyCredential(admin_key))

def get_promt_with_source(user_prompt, openai_api_key):
    """
    Generates a search query using OpenAI based on the user's prompt, performs a search using Azure Cognitive Search,
    and formats the results to be used as context for generating an answer.

    Args:
        user_prompt (str): The user's input prompt.
        openai_api_key (str): The API key for OpenAI.

    Returns:
        str: A prompt including the user's original question and information from the top search results,
             ready to be used for generating an answer with OpenAI.
    """

    # Generate an optimized search query with OpenAI.
    optimized_query = generate_openai_response(user_prompt, openai_api_key, query_prompt_template)

    if optimized_query == '0':
        print('Can\'t generate a search query')
        optimized_query = user_prompt  # Fallback to the original user prompt if unable to optimize.

    # Perform the search with the generated or fallback query, limiting results.
    # Adjust 'top' for more or fewer results, but be mindful of !!Token Usage !! and performance.
    results = list(search_client.search(search_text=optimized_query, include_total_count=True, top=3))

    sources_content, citations = get_sources_content(results)
    content = "\n".join(sources_content)

    prompt = f"""The user asked: "{user_prompt}".\n\nBased on the following sources, provide a concise yet comprehensive answer:\n{content}\n\nAnswer:"""
    return prompt, citations

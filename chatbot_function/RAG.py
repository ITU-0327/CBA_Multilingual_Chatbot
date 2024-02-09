from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
import os

from .openai_service import generate_openai_response
from .utils import get_sources_content


service_name = os.environ["SERVICE_NAME"]
admin_key = os.environ["ADMIN_KEY"]
index_name = os.environ["INDEX_NAME"]

query_prompt_template = """Below is a history of the conversation so far, and a new question asked by the user that needs to be answered by searching in a knowledge.
You have access to Azure AI Search index with 100's of documents.
Generate a search query based on the conversation and the new question.
Do not include cited source filenames and document names e.g info.txt or doc.pdf in the search query terms.
Do not include any text inside [] or <<>> in the search query terms.
Do not include any special characters like '+'.
If the question is not in English, translate the question to English before generating the search query.
If you cannot generate a search query, return just the number 0.
"""

endpoint = f"https://{service_name}.search.windows.net/"

search_client = SearchClient(endpoint=endpoint,
                             index_name=index_name,
                             credential=AzureKeyCredential(admin_key))


def get_promt_with_source(user_prompt, openai_api_key):
    optimized_query = generate_openai_response(user_prompt, openai_api_key, query_prompt_template)
    # print(f"Optimized Query: {optimized_query}")

    if optimized_query == '0':
        print('Can\'t generate a search query')
        optimized_query = user_prompt

    results = list(search_client.search(search_text=optimized_query, include_total_count=True, top=3))

    # print(f'Total Documents Matching Query: {len(results)}')

    # for result in results:
    #     print(f"{result['id']}: {result.get('title', 'No Title')}")

    sources_content = get_sources_content(results)
    content = "\n".join(sources_content)

    prompt = f"""The user asked: "{user_prompt}".\n\nBased on the following sources, provide a detailed answer:\n{content}\n\nAnswer:"""
    return prompt
    
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os
from typing import List

def get_secret(secret_name):
    key_vault_name = os.environ["KEY_VAULT_NAME"]
    key_vault_uri = f"https://{key_vault_name}.vault.azure.net/"

    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_uri, credential=credential)
    retrieved_secret = client.get_secret(secret_name)

    return retrieved_secret.value


def get_sources_content(docs):
    formatted_docs = []
    for doc in docs:
        citation = doc.get('url', '')
        
        content_parts = [doc.get('title', ''), nonewlines(doc.get('content', ''))]
        
        content_parts += [section['text'] for section in doc.get('sections', []) if section['text']]
        
        content = " . ".join(content_parts)
        
        formatted_content = f"{citation}: {content}"
        
        formatted_docs.append(formatted_content)
    
    return formatted_docs


def nonewlines(text: str) -> str:
    return ' '.join(text.split())

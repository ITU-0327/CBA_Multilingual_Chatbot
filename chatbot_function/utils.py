from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os
from typing import List


def get_secret(secret_name: str) -> str:
    """
    Retrieves the value of a secret from Azure Key Vault.

    This function requires an environment variable `KEY_VAULT_NAME` to be set, which is the name of the Key Vault
    from which to fetch the secret.
    For local development, this can be set in `local.settings.json`.
    For production use Settings/Configuration in Function App.

    Args:
        secret_name (str): The name of the secret to retrieve.

    Returns:
        str: The value of the retrieved secret.
    """

    key_vault_name = os.environ["KEY_VAULT_NAME"]
    key_vault_uri = f"https://{key_vault_name}.vault.azure.net/"

    # Authenticate using the default Azure credential method.
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_uri, credential=credential)

    retrieved_secret = client.get_secret(secret_name)

    return retrieved_secret.value


def get_sources_content(docs: List[dict]) -> List[str]:
    """
    Formats a list of document dictionaries into a list of strings containing the content.

    Each document dictionary should have 'url', 'title', 'content', and optionally 'sections'.
    Sections should be a list of dictionaries with a 'text' field.

    Args:
        docs (List[dict]): A list of document dictionaries to format.

    Returns:
        List[str]: A list of formatted strings containing the content from the input documents.
    """

    formatted_docs = []
    for doc in docs:
        url = doc.get('url', '')
        
        content_parts = [doc.get('title', ''), nonewlines(doc.get('content', ''))]
        
        content_parts += [section['text'] for section in doc.get('sections', []) if section['text']]
        
        # Concatenate all parts, separated by periods.
        content = " . ".join(content_parts)
        
        formatted_content = f"{url}: {content}"
        
        formatted_docs.append(formatted_content)

    citations = [doc.get('url', '') for doc in docs]
    
    return formatted_docs, citations


def nonewlines(text: str) -> str:
    """
    Removes all newline characters from a string, replacing them with spaces.

    Args:
        text (str): The input string from which to remove newline characters.

    Returns:
        str: The modified string with newline characters replaced by spaces.
    """
    return ' '.join(text.split())

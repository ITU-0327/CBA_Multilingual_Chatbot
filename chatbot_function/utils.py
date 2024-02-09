from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

def get_secret(secret_name):
    key_vault_name = os.environ["KEY_VAULT_NAME"]
    key_vault_uri = f"https://{key_vault_name}.vault.azure.net/"

    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_uri, credential=credential)
    retrieved_secret = client.get_secret(secret_name)

    return retrieved_secret.value


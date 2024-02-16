from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import os
import requests, uuid, json

from .utils import get_secret


language_service_key = get_secret('language-service-key')
endpoint = os.environ["AZURE_LANGUAGE_SERVICE_ENDPOINT"]


def authenticate_client():
    ta_credential = AzureKeyCredential(language_service_key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client


def detect_language(input_text: str) -> str:
    """
    Detects the primary language of the given input text using Azure's Text Analytics API.

    If the input text is empty or contains only whitespace, the function returns 'und' to
    indicate an undefined language, as making a call with empty content could be wasteful
    or lead to unnecessary processing.

    Args:
        input_text (str): The text for which to detect the language.

    Returns:
        str: The ISO 639-1 language code of the detected primary language, or 'und' if the
        input text is empty or cannot be processed.
    """
    if not input_text.strip():
        return 'und'

    client = authenticate_client()
    
    try:
        response = client.detect_language(documents=[input_text])[0]
        return response.primary_language.iso6391_name
    except Exception as err:
        print(f"Encountered exception: {err}")
        return 'und'


def translate_text(input_text: str, from_lang: str = 'en', to_lang: str = 'fr') -> str:
    """
    Translates text from one language to a specified target language using Azure's Translator Text API.

    Args:
        input_text (str): The text to be translated.
        from_lang (str): The source language code (default is 'en' for English).
        to_lang (str): The target language code (e.g., 'fr' for French).

    Returns:
        str: A JSON string of the translation results.
    """

    key = None
    endpoint = None
    location = "australiaeast"

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': from_lang,
        'to': to_lang
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{'text': input_text}]

    response = requests.post(constructed_url, params=params, headers=headers, json=body).json()

    return json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': '))

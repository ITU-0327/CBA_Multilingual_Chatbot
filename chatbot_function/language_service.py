from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import os
import requests, uuid, json

from .utils import get_secret


key = get_secret('detect-language')
endpoint = os.environ["AZURE_TRANSLATE_ENDPOINT"]
location = "australiaeast"


def detect_language(input_text: str) -> str:
    """
    Detects the primary language of the given input text using Azure's Translator Text API.

    Args:
        input_text (str): The text for which to detect the language.

    Returns:
        str: The detected language code (e.g., 'de' for German).
    """

    path = '/detect'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0'
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': input_text
    }]

    try:
        request = requests.post(constructed_url, params=params, headers=headers, json=body)
        response = request.json()

        detected_language = response[0]["language"]
        return detected_language
    except Exception as err:
        print(f"Encountered exception: {err}")
        return 'und'


def translate_text(input_text: str, from_lang: str = '', to_lang: str = 'en') -> str:
    """
    Translates text from one language to a specified target language using Azure's Translator Text API.

    Args:
        input_text (str): The text to be translated.
        from_lang (str): The source language code (default is 'en' for English).
        to_lang (str): The target language code (e.g., 'fr' for French).

    Returns:
        str: A JSON string of the translation results.
    """

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
    try:
        translations = response[0]['translations']
        translated_text = translations[0]['text'] if translations else ""
    except Exception as err:
        return f"Encountered exception: {err}"

    return translated_text

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.document import DocumentTranslationClient, TranslationTarget
from .utils import get_secret
import os


# Initialise Azure Cognitive Services credentials
endpoint = os.environ["AZURE_LANGUAGE_SERVICE_ENDPOINT"]
language_service_key = get_secret('language-service-key')


# Function to create a Text Analytics Client
def authenticate_client():
    ta_credential = AzureKeyCredential(language_service_key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

def detect_language(input_text):
    client = authenticate_client()
    response = client.detect_language(documents=[{"id": "1", "text": input_text}])
    
    if response is not None and len(response) > 0:
        for document in response:
            if 'primary_language' in document:
                language = document['primary_language']['iso6391_name']
                return(language)
            else:
                return("No language detected.")
    else:
        return("No language detected.")


# Function to translate text
def translate_text(input_text, target_language="en"):
    document_translation_client = DocumentTranslationClient(endpoint, AzureKeyCredential(language_service_key))
    
    # For the sake of simplicity in this example, we'll pretend there's a function that submits
    # translation jobs and waits for the result, returning the translated text.
    translated_text = submit_translation_job_and_wait(document_translation_client, input_text, target_language)
    
    return translated_text

# Dummy function for translation job submission
# Replace this with actual logic to use Azure's Document Translation
def submit_translation_job_and_wait(client, input_text, target_language):
    # Implement the job submission and waiting logic here
    # This is a placeholder function
    return "translated text"  # Placeholder return value

# Ensure to handle authentication and error management in production code appropriately

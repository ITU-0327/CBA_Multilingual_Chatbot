from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.document import DocumentTranslationClient, TranslationTarget
import os

# from .utils import get_secret


# language_service_key = get_secret('language-service-key')
# endpoint = os.environ["AZURE_LANGUAGE_SERVICE_ENDPOINT"]


# def authenticate_client():
#     ta_credential = AzureKeyCredential(language_service_key)
#     text_analytics_client = TextAnalyticsClient(
#             endpoint=endpoint, 
#             credential=ta_credential)
#     return text_analytics_client


# def detect_language(input_text: str) -> str:
#     """
#     Detects the primary language of the given input text using Azure's Text Analytics API.

#     If the input text is empty or contains only whitespace, the function returns 'und' to
#     indicate an undefined language, as making a call with empty content could be wasteful
#     or lead to unnecessary processing.

#     Args:
#         input_text (str): The text for which to detect the language.

#     Returns:
#         str: The ISO 639-1 language code of the detected primary language, or 'und' if the
#         input text is empty or cannot be processed.
#     """
#     if not input_text.strip():
#         return 'und'

#     client = authenticate_client()
    
#     try:
#         response = client.detect_language(documents=[input_text])[0]
#         return response.primary_language.iso6391_name
#     except Exception as err:
#         print(f"Encountered exception: {err}")
#         return 'und'

endpoint = "https://cba-languageservice.cognitiveservices.azure.com/"
language_service_key = "0e28e50d295144e0811dd4c36aabf286"
# Function to translate text
def translate_text(input_text, target_language="en"):
    document_translation_client = DocumentTranslationClient(endpoint, AzureKeyCredential(language_service_key))

    try:
        # Submit translation job
        poller = document_translation_client.begin_translation(inputs=[{"text": input_text}], target_language=target_language, source_language="en")
        
        # Wait for translation job to complete
        result = poller.result()
        
        # Extract translated text from the result
        translated_text = result[0].translations[0].translated_text
        
        return translated_text
    except Exception as err:
        print(f"Encountered exception during translation: {err}")
        return None

# Example usage
if __name__ == "__main__":
    # Input text to be translated
    input_text = input("Enter the text you want to translate: ")

    # Translate the input text
    translated_text = translate_text(input_text)

    # Print the translated text
    print("Translated text:", translated_text)



# Dummy function for translation job submission
# Replace this with actual logic to use Azure's Document Translation
def submit_translation_job_and_wait(client, input_text, target_language):
    # Implement the job submission and waiting logic here
    # This is a placeholder function
    return "translated text"  # Placeholder return value

# Ensure to handle authentication and error management in production code appropriately

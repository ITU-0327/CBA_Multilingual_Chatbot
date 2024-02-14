from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.document import DocumentTranslationClient, TranslationTarget
import os

subscription_key = "b0850fb413f048169de90fff4584b65a"
endpoint = "YOUR_TRANSLATOR_ENDPOINT"



# Initialise Azure Cognitive Services credentials
# key = os.environ["AZURE_LANGUAGE_SERVICE_KEY"]
# endpoint = os.environ["AZURE_LANGUAGE_SERVICE_ENDPOINT"]
key = "b0850fb413f048169de90fff4584b65a"
endpoint = "https://cba-translator.cognitiveservices.azure.com/"

credential = AzureKeyCredential(subscription_key)
translator_client = TextAnalyticsClient(endpoint, credential)

# Function to create a Text Analytics Client
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

# Function to detect language
def detect_language(input_text):
    client = authenticate_client()
    response = client.detect_language(documents=[{"id": "1", "text": input_text}])
    if response is not None and len(response.documents) > 0:
        return response.documents[0].primary_language.iso6391_name
    return "en"  # Default to English if detection fails

# Test input text samples
input_texts = [
    "Hello, how are you?",
    "Bonjour, comment ça va?",
    "Hola, ¿cómo estás?",
    "Guten Tag, wie geht es Ihnen?",
    "こんにちは、元気ですか？",
    "안녕하세요, 잘 지내세요?",
    "你好吗？",
    "مرحبا، كيف حالك؟"
]

# Call the detect_language function for each input text
for text in input_texts:
    detected_language = detect_language(text)
    print(f"Input Text: '{text}' | Detected Language: {detected_language}")

# Test an edge case with an empty string
empty_text = ""
detected_language_empty = detect_language(empty_text)
print(f"Empty Text | Detected Language: {detected_language_empty}")


# Function to translate text
def translate_text(input_text, target_language="en"):
    document_translation_client = DocumentTranslationClient(endpoint, AzureKeyCredential(key))
    
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

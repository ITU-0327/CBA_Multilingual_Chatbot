from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.document import DocumentTranslationClient, TranslationTarget
import os


# Initialise Azure Cognitive Services credentials
# key = os.environ["AZURE_LANGUAGE_SERVICE_KEY"]
# endpoint = os.environ["AZURE_LANGUAGE_SERVICE_ENDPOINT"]
key = "0e28e50d295144e0811dd4c36aabf286"
endpoint = "https://cba-languageservice.cognitiveservices.azure.com/"


# Function to create a Text Analytics Client
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
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
                print(f"Detected Language: {language}")
            else:
                print("No language detected.")
    else:
        print("No language detected.")

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
    detect_language(text)

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

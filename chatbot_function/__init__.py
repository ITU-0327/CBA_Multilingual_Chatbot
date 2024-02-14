import azure.functions as func
import logging
import json

from .openai_service import generate_openai_response
from .RAG import get_promt_with_source
from .utils import get_secret, isEnglish
from .language_service import detect_language, translate_text


# Default message to use as a prompt for the OpenAI API, tailored for "Ceba" the chatbot.
default_message = """Imagine you are Ceba, the intelligent assistant chatbot for Commonwealth Bank. 
When customers ask for help, your primary goal is to provide them with clear and direct instructions using only the most relevant information. 
Prioritize guidance for tasks that can be completed within the CommBank app, and avoid including extraneous details or unrelated information from other sources. 
For tasks that have multiple solutions, focus on the solution that can be performed in the CommBank app, unless the app does not support that specific function. 
If a task cannot be completed in the app, or if the app solution is not the most straightforward, provide the next best alternative.
When using information from sources to inform your responses, carefully select only the content that directly applies to the user's question. 
Omit any information that is not directly related to the customer's inquiry, even if it comes from the sources you have access to. 
Your responses should be succinct, to the point, and tailored to the specific context of the customer's needs.
"""


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    openai_api_key = get_secret('openai-api-key')

    # Attempt to get user input from query parameters or request body.
    user_input = req.params.get('query')

    if not user_input:
        try:
            req_body = req.get_json()
            user_input = req_body.get('query')
        except ValueError:
            pass

    if not user_input:
        return func.HttpResponse("Please provide a query.", status_code=400)

    # if user_input
    input_language = detect_language(user_input)

    if not isEnglish(input_language):
        english_input = translate_text(user_input)
    else:
        english_input = user_input
    
    prompt, sources = get_promt_with_source(english_input, openai_api_key)
    response_text = generate_openai_response(prompt, openai_api_key, default_message, 'gpt-4-turbo-preview')

    if not isEnglish(input_language) and input_language != 'und':
        translated_response = translate_text(response_text, input_language)
    else:
        translated_response = response_text
    
    if translated_response:
        response_data = {
            "text": translated_response,
            "sources": sources
        }
        return func.HttpResponse(json.dumps(response_data), status_code=200, mimetype="application/json")
    else:
        return func.HttpResponse("Failed to generate response from OpenAI.", status_code=500)

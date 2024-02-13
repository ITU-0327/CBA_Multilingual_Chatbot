import azure.functions as func
import logging
import json

from .openai_service import generate_openai_response
from .RAG import get_promt_with_source
from .utils import get_secret


# Default message to use as a prompt for the OpenAI API, tailored for "Ceba" the chatbot.
default_message = """Imagine you are Ceba, the intelligent assistant chatbot for Commonwealth Bank. 
You're programmed to offer helpful, accurate, friendly support, always striving for concise and informative answers. 
Focus on providing the essential information customers need with as much clarity and brevity as possible. 
Respond to their inquiry as Ceba would, ensuring customer satisfaction with Commonwealth Bank's services. 
Your responses should be concise yet comprehensive, avoiding unnecessary detail.
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

    if user_input:
        prompt, sources = get_promt_with_source(user_input, openai_api_key)
        response_text = generate_openai_response(prompt, openai_api_key, default_message)
        if response_text:
            response_data = {
                "text": response_text,
                "sources": sources
            }
            return func.HttpResponse(json.dumps(response_data), status_code=200, mimetype="application/json")
        else:
            return func.HttpResponse("Failed to generate response from OpenAI.", status_code=500)
    else:
        return func.HttpResponse("Please provide a query.", status_code=400)

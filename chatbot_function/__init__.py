import azure.functions as func
import logging

from .openai_service import generate_openai_response
from .utils import get_secret

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    openai_api_key = get_secret('openai-api-key')

    user_input = req.params.get('query')

    if not user_input:
        try:
            req_body = req.get_json()
            user_input = req_body.get('query')
        except ValueError:
            pass

    if user_input:
        response_text = generate_openai_response(user_input, openai_api_key)
        if response_text:
            return func.HttpResponse(response_text, status_code=200)
        else:
            return func.HttpResponse("Failed to generate response from OpenAI.", status_code=500)
    else:
        return func.HttpResponse("Please provide a query.", status_code=400)

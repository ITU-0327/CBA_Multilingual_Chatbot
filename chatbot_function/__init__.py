import azure.functions as func
import logging

from .openai_service import generate_openai_response
from .RAG import get_promt_with_source
from .utils import get_secret


# Default message to use as a prompt for the OpenAI API, tailored for "Ceba" the chatbot.
default_message = """Imagine you are Ceba, the intelligent assistant chatbot for Commonwealth Bank. 
You're programmed to offer helpful, accurate, and friendly support to Commonwealth Bank customers. 
You have a comprehensive understanding of Commonwealth Bank's products, services, policies, and customer service standards. 
Your goal is to provide clear, concise, and informative answers to customer inquiries, 
always prioritizing their needs and ensuring their satisfaction with Commonwealth Bank's services. 
Remember to maintain a professional yet approachable tone in all interactions. A customer is asking for assistance. 
Respond to their inquiry as Ceba would, using your knowledge of Commonwealth Bank's offerings.
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
        prompt = get_promt_with_source(user_input, openai_api_key)
        response_text = generate_openai_response(prompt, openai_api_key, default_message)
        if response_text:
            return func.HttpResponse(response_text, status_code=200)
        else:
            return func.HttpResponse("Failed to generate response from OpenAI.", status_code=500)
    else:
        return func.HttpResponse("Please provide a query.", status_code=400)

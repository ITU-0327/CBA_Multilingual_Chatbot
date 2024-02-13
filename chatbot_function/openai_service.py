from openai import OpenAI


def generate_openai_response(prompt_text: str, openai_api_key: str, system_message: str) -> str:
    """
    Args:
        prompt_text (str): The user's input text to which the model should respond.
        openai_api_key (str): The API key for authenticating requests to OpenAI.
        system_message (str): A system-level message that provides context for the conversation. 
                              This is used to prime the model for generating responses in a specific context.

    Returns:
        str or None: The generated response from the model, or None if an error occurs during the API call.

    Raises:
        Prints an error message to the console if the OpenAI API call fails.
    """
    
    client = OpenAI(api_key=openai_api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Specify the model to use.
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt_text},
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None

from openai import OpenAI
import os


openai_api_key = os.environ.get("OpenAI_ApiKey")


def generate_openai_response(prompt_text, openai_api_key):
    client = OpenAI(api_key=openai_api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt_text},
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None


input = "Hello what can you help me"
print(generate_openai_response(input, openai_api_key))

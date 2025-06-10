import os
from dotenv import load_dotenv
import together

load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

together.api_key = TOGETHER_API_KEY

def generate_email(prompt):
    try:
        response = together.Complete.create(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            prompt=f"You are a professional email assistant. {prompt}",
            max_tokens=500,
            temperature=0.7,
        )   

        return response['choices'][0]['text'].strip()
    except Exception as e:
        return f"Error: {e}"



import os
from fastapi import HTTPException
import google.generativeai as genai


genai.configure(api_key=os.getenv("API_KEY"))

def text_summarization(text):
    try:
        # Use the ChatCompletion API to generate a summary
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f'Summarize this {text}')
        print(response.text)
    except Exception as e:
        # Handle exceptions and raise an HTTPException
        raise HTTPException(status_code=500, detail=f"Error in summarization: {str(e)}")
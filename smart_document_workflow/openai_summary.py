import os
from fastapi import HTTPException
import google.generativeai as genai


genai.configure(api_key=os.getenv("API_KEY"))

def text_summarization(text, text_request):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        text_prompt = text_request + "\n" + text
        response = model.generate_content(text_prompt)
        return response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in summarization: {str(e)}")
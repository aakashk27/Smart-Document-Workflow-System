import os
from fastapi import HTTPException
import google.generativeai as genai


genai.configure(api_key=os.getenv("API_KEY"))

def text_summarization(text):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f'Summarize this {text}', )
        print(response.to_dict())
        return response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in summarization: {str(e)}")
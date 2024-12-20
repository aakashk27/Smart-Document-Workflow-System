from pdf2image import convert_from_path
from PIL import Image
import pytesseract
from fastapi import HTTPException
import os

def extract_text_from_file(file_path: str) -> str:
    """
    Extract text from an image or PDF using Tesseract OCR.
    """
    try:
        if not os.path.exists(file_path):
            raise HTTPException(status_code=500, detail=f"File not found: {file_path}")

        os.environ["PATH"] += os.pathsep + "/opt/homebrew/bin"

        if file_path.lower().endswith(".pdf"):
            images = convert_from_path(file_path, poppler_path="/opt/homebrew/bin")
            extracted_text = ""
            for page_number, image in enumerate(images):
                extracted_text += pytesseract.image_to_string(image)
                extracted_text += "\n\n"
            return extracted_text.strip()
        else:
            img = Image.open(file_path)
            return pytesseract.image_to_string(img).strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in OCR processing: {str(e)}")

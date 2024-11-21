import pytesseract
from PIL import Image
from fastapi import HTTPException

def extract_text_from_image(file_path: str) -> str:
    """
    Extract text from an image using Tesseract OCR.
    """
    try:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in OCR processing: {str(e)}")

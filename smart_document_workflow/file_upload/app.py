from typing import Annotated
from fastapi import Body, Depends, FastAPI, UploadFile, File, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pymongo import MongoClient
from bson import ObjectId
from config import Config
from werkzeug.utils import secure_filename
from file_upload.models import DocumentModel, UploadResponse
import os
import aiofiles
import asyncio

from nlp import extract_entities
from ocr import extract_text_from_file
from openai_summary import text_summarization
from auth.services import verify_access_token
from file_upload.get_pdf_from_text import get_pdf

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# MongoDB connection
client = MongoClient(Config.MONGO_URI)
db = client.smart_documents
documents_collection = db.documents

# Set up upload folder
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


async def upload_document(*, file: UploadFile = File(...), text: str = Body(..., embed=True)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    text_request = text

    try:
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

    document_data = DocumentModel(filename=filename, file_path=file_path)
    inserted_document = documents_collection.insert_one(document_data.model_dump())
    document_id = str(inserted_document.inserted_id)

    try:
        text_from_file = await extract_text_from_file_async(file_path)
        entities = await extract_entities_from_file(text_from_file)
        summarization = await summarize_text_async(text_from_file, text_request)
        if len(summarization) > 2000:
            get_pdf(summarization)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

    try:
        filter = {"_id": ObjectId(document_id)}
        documents_collection.update_one(
            filter,
            {
                "$set": {
                    "processing_results": {
                        "text": text_from_file[:300],
                        "summarization": summarization,
                        "entities": entities,
                    }
                }
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database update error: {str(e)}")

    return UploadResponse(
        message="Uploaded successfully",
        file_data={**document_data.model_dump(), "_id": document_id}
    )


async def extract_text_from_file_async(file_path: str) -> str:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, extract_text_from_file, file_path)


async def summarize_text_async(text: str, text_request: str) -> str:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, text_summarization, text, text_request)


async def extract_entities_from_file(text: str) -> dict:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, extract_entities, text)

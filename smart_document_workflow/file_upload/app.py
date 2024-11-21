from fastapi import FastAPI, UploadFile, File, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from config import Config
from werkzeug.utils import secure_filename
from file_upload.models import DocumentModel, UploadResponse
import os

from nlp import extract_entities
from ocr import extract_text_from_image

# MongoDB connection
client = MongoClient(Config.MONGO_URI)
db = client.smart_documents  # Database name
documents_collection = db.documents  # Collection name

# Set up upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


async def upload_document(file: UploadFile = File(...)):
    # Check for file presence
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    # Secure and save file
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    text_from_file = extract_text_from_image(file_path)
    entities_from_file = extract_entities(text_from_file)
    
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Create document data using the model
    document_data = DocumentModel(filename=filename, file_path=file_path,  processing_results={
            "text": text_from_file,
            "entities": entities_from_file,
        })

    # Insert the document into MongoDB
    inserted_document = documents_collection.insert_one(document_data.model_dump())
    document_id = str(inserted_document.inserted_id)

    # Add the `_id` field to the response
    return UploadResponse(
        message="Uploaded successfully",
        file_data={**document_data.model_dump(), "_id": document_id}
    )

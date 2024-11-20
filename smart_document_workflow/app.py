# app.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from bson import ObjectId
from config import Config
import os
from werkzeug.utils import secure_filename

# Initialize FastAPI app
app = FastAPI()

# MongoDB connection
client = MongoClient(Config.MONGO_URI)
db = client.smart_documents  # Database name
documents_collection = db.documents  # Collection name

print('!!!!', documents_collection)

# Set up upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    print('file is ', file.__dict__)
    # Check for file presence
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    # Secure and save file
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Insert document metadata into MongoDB
    document_data = {
        'filename': filename,
        'file_path': file_path,
        'status': 'Uploaded',
        'processing_results': None
    }
    inserted_document = documents_collection.insert_one(document_data)

    document_data["_id"] = str(inserted_document.inserted_id)

    return JSONResponse(content={"message": "File uploaded successfully!", "file_data": document_data}, status_code=200)

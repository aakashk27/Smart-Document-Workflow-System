import datetime
from pydantic import BaseModel
from typing import Optional


class DocumentModel(BaseModel):
    filename: str
    file_path: str
    status: str = 'Uploaded'
    created_at: datetime.datetime = datetime.datetime.now()
    processing_results: Optional[dict[str,str]] = None


class UploadResponse(BaseModel):
    message: str
    file_data: DocumentModel
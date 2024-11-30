import datetime
from pydantic import BaseModel, Field
from typing import Optional


class DocumentModel(BaseModel):
    filename: str
    file_path: str
    status: str = 'Uploaded'
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    processing_results: dict = Field(default_factory=dict)


class UploadResponse(BaseModel):
    message: str
    file_data: DocumentModel
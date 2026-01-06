from pydantic import BaseModel
from datetime import datetime

class SubmissionCreate(BaseModel):
    code: str
    question_id: int

class SubmissionResponse(SubmissionCreate):
    id: int
    user_id: int
    created_at: datetime
    status: str | None = None
    detailed_results: dict | None = None

    class Config:
        from_attributes = True
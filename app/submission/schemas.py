from pydantic import BaseModel
from datetime import datetime
from typing import List
from app.questions.schemas import TestCaseBase

class SubmissionCreate(BaseModel):
    code: str
    question_id: int
    status: str | None = "Not Submitted"
    detailed_results: list | dict | None = None

class SubmissionResponse(SubmissionCreate):
    id: int
    user_id: int
    created_at: datetime
    status: str | None = None
    username: str | None = None
    full_name: str | None = None
    question_title: str | None = None
    test_cases: List[TestCaseBase] | None = None
    detailed_results: dict | None = None

    class Config:
        from_attributes = True
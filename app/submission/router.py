from fastapi import APIRouter, Depends, HTTPException
from app.submission.schemas import SubmissionCreate, SubmissionResponse
from app.core import database
from app.auth.utils import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.submission import crud
from app.user.models import User

router = APIRouter()






@router.post("/", response_model=SubmissionResponse)  # type: ignore
async def create_submission(
    submission_data: SubmissionCreate,
    db: AsyncSession = Depends(database.get_db), # type: ignore
    current_user: User = Depends(get_current_user)
):
    return await crud.create_submission(db, submission_data, current_user.id) # type: ignore


@router.get("/latest/{question_id}", response_model=SubmissionResponse)  # type: ignore
async def get_latest_submission(
    question_id: int,
    db: AsyncSession = Depends(database.get_db), # type: ignore
    current_user: User = Depends(get_current_user)
):
    latest_submission = await crud.get_latest_submission(db, current_user.id, question_id) # type: ignore
    if not latest_submission:
        raise HTTPException(status_code=404, detail="No submissions found for this question.")
    return latest_submission

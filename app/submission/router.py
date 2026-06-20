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


@router.get("/by_question/{question_id}", response_model=list[SubmissionResponse])  # type: ignore
async def get_submissions_by_question(
    question_id: int,
    db: AsyncSession = Depends(database.get_db), # type: ignore
):
    submissions = await crud.get_submission_by_question_id(db, question_id) # type: ignore
    if not submissions:
        raise HTTPException(status_code=404, detail="No submissions found for this question.")
    return submissions


@router.get("/{submission_id}", response_model=SubmissionResponse)  # type: ignore
async def get_submission_by_id(
    submission_id: int,
    db: AsyncSession = Depends(database.get_db), # type: ignore
):
    submission = await crud.get_submission_by_id(db, submission_id) # type: ignore
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found.")
    return submission

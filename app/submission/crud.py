from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.submission.models import Submission
from app.submission.schemas import SubmissionCreate
from datetime import datetime, timezone


async def create_submission(db: AsyncSession, submission_data: SubmissionCreate, user_id: int):
    latest_submission = await get_latest_submission(db, user_id, submission_data.question_id)
    
    query_passed = (
        select(Submission)
        .where(Submission.user_id == user_id, 
               Submission.question_id == submission_data.question_id, 
               Submission.status == "Passed")
    )
    result_passed = await db.execute(query_passed)
    has_passed_before = result_passed.scalars().first()
    
    final_status = submission_data.status
    if has_passed_before:
        final_status = "Passed"

    if (
        submission_data.status == "on progress"
        and latest_submission
        and latest_submission.status == "on progress"  # type: ignore
    ):
        latest_submission.code = submission_data.code  # type: ignore
        latest_submission.detailed_results = submission_data.detailed_results  # type: ignore
        latest_submission.created_at = datetime.now(timezone.utc).replace(tzinfo=None)  # type: ignore

        await db.commit()
        await db.refresh(latest_submission)
        return latest_submission

    new_submission = Submission(
        code=submission_data.code,
        question_id=submission_data.question_id,
        user_id=user_id,
        detailed_results=submission_data.detailed_results,
        status=final_status, 
        created_at=datetime.now(timezone.utc).replace(tzinfo=None),
    )

    db.add(new_submission)
    await db.commit()
    await db.refresh(new_submission)
    return new_submission


async def get_latest_submission(db: AsyncSession, user_id: int, question_id: int):
    query = (
        select(Submission)
        .where(Submission.user_id == user_id, Submission.question_id == question_id)
        .order_by(desc(Submission.created_at))
        .limit(1)
    )

    result = await db.execute(query)
    latest_submission = result.scalars().first()
    return latest_submission
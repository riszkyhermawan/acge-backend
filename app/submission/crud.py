from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.submission.models import Submission
from app.submission.schemas import SubmissionCreate
from datetime import datetime, timezone


async def create_submission(db: AsyncSession, submission_data: SubmissionCreate, user_id: int):
    new_submission = Submission(
        code = submission_data.code,
        question_id = submission_data.question_id,
        user_id = user_id,
        created_at = datetime.now(timezone.utc).replace(tzinfo=None)
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
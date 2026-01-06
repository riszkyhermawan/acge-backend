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
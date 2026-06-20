from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.submission.models import Submission
from app.submission.schemas import SubmissionCreate
from datetime import datetime, timezone
from collections import defaultdict
from app.questions.models import TestCases 


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


async def get_submission_by_question_id(db: AsyncSession, question_id: int):
    query = (
        select(Submission)
        .where(Submission.question_id == question_id)
        .options(joinedload(Submission.user))  # Eager load the related User
        .order_by(desc(Submission.created_at))
    )
    
    result = await db.execute(query)
    submissions = result.scalars().all()
    
    submissions_by_user = defaultdict(list)
    for submission in submissions:
        submissions_by_user[submission.user_id].append(submission)
    
    submission_per_user = []
    for user_id, user_submissions in submissions_by_user.items():
        passed = [s for s in user_submissions if s.status == "Passed"]
        if passed:
            best_passed = max(passed, key=lambda s: s.created_at)
        else:
            best_passed = user_submissions[0]
            
        submission_per_user.append(best_passed)
    
    return [
        {
            **submission.__dict__,
            "username": submission.user.username if submission.user else None,  # type: ignore
            "full_name": submission.user.full_name if submission.user else None,  # type: ignore
        }
        for submission in sorted(submission_per_user, key=lambda s: s.created_at if s else datetime.min, reverse=True)
    ]
    
    
async def get_submission_by_id(db: AsyncSession, submission_id: int):
    query = (
        select(Submission)
        .where(Submission.id == submission_id)
        .options(
            joinedload(Submission.user),
            joinedload(Submission.question)
        )
    )
    
    result = await db.execute(query)
    submission = result.scalars().first()
    
    if not submission:
        return None
    
    # Fetch test cases separately
    test_cases_query = select(TestCases).where(TestCases.question_id == submission.question_id) # type: ignore
    test_cases_result = await db.execute(test_cases_query)
    test_cases = test_cases_result.scalars().all()
    
    return {
        "id": submission.id,
        "code": submission.code,
        "question_id": submission.question_id,
        "user_id": submission.user_id,
        "status": submission.status,
        "created_at": submission.created_at,
        "detailed_results": submission.detailed_results,
        "username": submission.user.username if submission.user else None,
        "full_name": submission.user.full_name if submission.user else None,
        "question_title": submission.question.title if submission.question else None,
        "test_cases": [
            {
                "id": tc.id,
                "input_data": tc.input_data, # type: ignore
                "expected_output": tc.expected_output, # type: ignore
            }
            for tc in test_cases
        ],
    }

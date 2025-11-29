from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.questions.models import Question, TestCases
from app.auth.utils import get_user_role
from app.questions.schemas import QuestionBase, TestCaseBase


async def create_question(db: AsyncSession, question_data: QuestionBase, test_cases: list[TestCaseBase], user_id: int):
    new_question = Question(
        title = question_data.title,
        description = question_data.description,
        attachment_url = question_data.attachment_url,
        created_by = user_id,
        test_cases = [TestCases(
            input_data = case.input_data,
            expected_output = case.expected_output,
        ) for case in test_cases]
    )
    db.add(new_question)
    await db.commit()
    await db.refresh(new_question)
    return new_question


async def get_question_by_id(db: AsyncSession, question_id: int):
    
    result = await db.get(Question, question_id)
    return result

async def update_question(db: AsyncSession, question_id: int, question_data: QuestionBase):
    question = await db.get(Question, question_id)
    if not question:
        return None
    question.title = question_data.title # type: ignore
    question.description = question_data.description # type: ignore
    question.attachment_url = question_data.attachment_url # type: ignore

    await db.commit()
    await db.refresh(question)
    return question

async def get_test_cases_by_question_id(db: AsyncSession, question_id: int):
    result = await db.execute(
        select(TestCases).where(TestCases.question_id == question_id)
    )
    test_cases = result.scalars().all()
    return test_cases

async def delete_questions(db: AsyncSession, question_id: int):
    question = await db.get(Question, question_id)
    if not question:
        return False
    await db.delete(question)
    await db.commit()
    return True

async def get_all_questions(db: AsyncSession):
    result = await db.execute(select(Question))
    questions = result.scalars().all()
    return questions

async def update_test_cases(db: AsyncSession, question_id: int, test_cases: list[TestCaseBase]):
    existing_test_cases = await get_test_cases_by_question_id(db, question_id)
    for existing_case in existing_test_cases:
        await db.delete(existing_case)
    await db.commit()
    
    new_test_cases = [
        TestCases(
            question_id = question_id,
            input_data = case.input_data,
            expected_output = case.expected_output
        ) for case in test_cases
    ]
    db.add_all(new_test_cases)
    await db.commit()
    return new_test_cases
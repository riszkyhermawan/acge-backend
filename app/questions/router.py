from fastapi import APIRouter, Depends, HTTPException
from app.questions.schemas import QuestionBase, TestCaseBase, QuestionResponse
from app.core import database
from app.auth.utils import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.questions import crud
from app.auth.utils import get_user_role

router = APIRouter()




########################################### QUESTION ROUTES ########################################
# Create Question
@router.post("/create", response_model=QuestionResponse)  # type: ignore
async def create_question(
    question_data: QuestionBase,
    db: AsyncSession = Depends(database.get_db), # type: ignore
    current_user: int = Depends(get_current_user), # type: ignore
    user_role: str = Depends(get_user_role)
):
    
    if user_role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can create questions.")
    else:
        return await crud.create_question(db, question_data, current_user.id) # type: ignore

# Update Question
@router.put("/{question_id}", response_model=QuestionResponse )  # type: ignore
async def update_question(
    question_id: int,
    question_data: QuestionBase,
    db: AsyncSession = Depends(database.get_db),  # type: ignore
    user_role: str = Depends(get_user_role)
):
    if user_role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can update questions.")
    else:
        updated_question = await crud.update_question(db, question_id, question_data) # type: ignore
        if not updated_question:
            raise HTTPException(status_code=404, detail="Question not found.")
        return updated_question

# Get All Questions
@router.get("/all", response_model=list[QuestionResponse])  # type: ignore
async def get_all_questions(
    db: AsyncSession = Depends(database.get_db)  # type: ignore
):
    questions = await crud.get_all_questions(db)
    response = []
    for question in questions:
        question_response = QuestionResponse(
            id = question.id,  # type: ignore
            title = question.title,  # type: ignore
            description = question.description,  # type: ignore
            attachment_url = question.attachment_url,  # type: ignore
        )
        response.append(question_response)
    return response


# Get Question by ID
@router.get("/{question_id}", response_model=QuestionResponse)  # type: ignore
async def get_question(
    question_id: int,
    db: AsyncSession = Depends(database.get_db)  # type: ignore
):
    question = await crud.get_question_by_id(db, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found.")
    test_cases = await crud.get_test_cases_by_question_id(db, question_id)
    
    result = QuestionResponse(
        id = question.id, # type: ignore
        title = question.title, # type: ignore
        description = question.description, # type: ignore
        attachment_url = question.attachment_url, # type: ignore
        test_cases = test_cases # type: ignore
    )
    return result
    

# Delete Question    
@router.delete("/{question_id}/delete", response_model=dict)  # type: ignore
async def delete_question(
    question_id: int,
    db: AsyncSession = Depends(database.get_db),  # type: ignore
    user_role: str = Depends(get_user_role)
):
    if user_role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can delete questions.")
    else:
        success = await crud.delete_questions(db, question_id)
        if not success:
            raise HTTPException(status_code=404, detail="Question not found.")
        return {"detail": "Question deleted successfully."}






######################################## TEST CASES ROUTES ########################################
#Update Test Cases
@router.put("/{question_id}/update-test-cases", response_model=list[TestCaseBase])  # type: ignore
async def update_test_cases(
    question_id: int,
    test_cases: list[TestCaseBase],
    db: AsyncSession = Depends(database.get_db),  # type: ignore
    user_role: str = Depends(get_user_role)
):
    if user_role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can update test cases.")
    else:
        updated_test_cases = await crud.update_test_cases(db, question_id, test_cases) # type: ignore
        return updated_test_cases
        
        

from pydantic import BaseModel, Field

class QuestionBase(BaseModel):
    title: str
    description: str = Field(..., max_length=1000)
    attachment_url: str | None = None
    
class TestCaseBase(BaseModel):
    input_data: dict
    expected_output: dict
    
    class Config:
        from_attributes = True
    

class QuestionResponse(QuestionBase):
    id: int
    test_cases: list[TestCaseBase] = []
    
    class Config:
        from_attributes = True
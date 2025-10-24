from pydantic import BaseModel, Field

class CodeRequest(BaseModel):
    source_code: str
    input_data: str = Field(default="")
from typing import Any, Dict
from pydantic import BaseModel, Field

class CodeRequest(BaseModel):
    source_code: str
    input_data: Dict[str, Any] = Field(default_factory=dict)
from fastapi import APIRouter, Depends, HTTPException
import httpx
from app.core.config import settings
from app.compiler.schema import CodeRequest
from app.auth.utils import get_user_role

router = APIRouter()


@router.post("/compile")
async def compile_code(request: CodeRequest, user_role: str = Depends(get_user_role)):
    code = request.source_code
    input_data = request.input_data 
    

    payload = {
        "source_code": code,
        "input_data": input_data
    }
    
    

    if user_role != "student":
        raise HTTPException(status_code=403, detail="Only students can compile code.")
    else:
        timeoutSetting = httpx.Timeout(30.0)
        async with httpx.AsyncClient(timeout=timeoutSetting) as client:
            try:
                response = await client.post(settings.COMPILER_API_URL, json=payload) # type: ignore
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                raise HTTPException(status_code=502, detail=f"Error communicating with compiler service: {str(e)}")
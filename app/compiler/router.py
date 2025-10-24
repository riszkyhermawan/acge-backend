from fastapi import APIRouter, Depends, HTTPException
import httpx
from app.core.config import settings
from app.compiler.schema import CodeRequest

router = APIRouter()


@router.post("/compile")
async def compile_code(request: CodeRequest):
    code = request.source_code
    input_data = request.input_data 
    
    payload = {
        "source_code": code,
        "input_data": input_data
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(settings.COMPILER_API_URL, json=payload) # type: ignore
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Error communicating with compiler service: {str(e)}")
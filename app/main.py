from sqlalchemy import text
from fastapi import Depends, FastAPI, HTTPException
from app.user import router as user_router
from app.auth import router as auth_router
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.compiler import router as compiler_router
import logging
import json
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.questions import router as question_router

app = FastAPI(title="ACGE Backend")
origins = settings.CLIENT_ORIGINS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# logging.basicConfig(
#     level=logging.DEBUG,  # or INFO in production
#     format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
# )
# logger = logging.getLogger("api_logger")

# class LoggingMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         # --- Log request ---
#         try:
#             body = await request.body()
#             body_text = body.decode("utf-8")
#         except Exception:
#             body_text = "<unreadable body>"

#         # redact sensitive headers
#         headers = dict(request.headers)
#         if "authorization" in headers:
#             headers["authorization"] = "[REDACTED]"

#         logger.debug(
#             "📥 Request:\n%s",
#             json.dumps(
#                 {
#                     "method": request.method,
#                     "url": str(request.url),
#                     "headers": headers,
#                     "body": body_text,
#                 },
#                 indent=2,
#             ),
#         )

#         # --- Process request ---
#         response = await call_next(request)

#         # --- Log response ---
#         try:
#             response_body = b""
#             async for chunk in response.body_iterator: # type: ignore
#                 response_body += chunk
#             # we must recreate the response because body_iterator is now consumed
#             response = response.__class__(
#                 content=response_body,
#                 status_code=response.status_code,
#                 headers=dict(response.headers),
#                 media_type=response.media_type,
#             )
#             body_preview = response_body.decode("utf-8")
#         except Exception:
#             body_preview = "<unreadable response body>"

#         logger.debug(
#             "📤 Response:\n%s",
#             json.dumps(
#                 {
#                     "status_code": response.status_code,
#                     "headers": dict(response.headers),
#                     "body": body_preview[:500],  # avoid dumping huge bodies
#                 },
#                 indent=2,
#             ),
#         )

#         return response


# # Register middleware
# app.add_middleware(LoggingMiddleware)



app.include_router(user_router.router, prefix="/users", tags=["users"])
app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
app.include_router(compiler_router.router, prefix="/compiler", tags=["compiler"])
app.include_router(question_router.router, prefix="/questions", tags=["questions"])


@app.get("/")
async def read_root():
    return {"message": "Buruaan kELARIN WOE SKRIPSI NYA ANJAY"}


@app.get("/health", tags=["health check"])
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        print(f"Database connection error: {e}")
        raise HTTPException(status_code=503, detail="Database connection error")
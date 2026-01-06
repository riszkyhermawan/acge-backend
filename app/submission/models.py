from sqlalchemy import Boolean, DateTime, Integer, String, Column, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.core.database import Base

class Submission(Base):
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    
    code = Column(String, nullable=False)
    status = Column(String, default="not submitted", nullable=False)
    created_at = Column(DateTime, nullable=False)
    detailed_results = Column(JSONB, nullable=True)
    
    user = relationship("User", back_populates="submissions", lazy="joined")
    question = relationship("Question", back_populates="submissions", lazy="joined")
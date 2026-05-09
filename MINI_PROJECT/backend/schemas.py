from pydantic import BaseModel, EmailStr
from typing import Optional, Any
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class CodeReviewRequest(BaseModel):
    code: str
    language: str

class CodeAnalysisResponse(BaseModel):
    general_explanation: str
    time_complexity_original: str
    line_by_line_explanation: str # JSON representation of line explanations
    optimized_code: Optional[str] = None
    time_complexity_optimized: Optional[str] = None
    optimization_explanation: Optional[str] = None

class CodeReviewResponse(BaseModel):
    id: int
    language: str
    original_code: str
    created_at: datetime
    analysis: Optional[CodeAnalysisResponse] = None

    class Config:
        from_attributes = True

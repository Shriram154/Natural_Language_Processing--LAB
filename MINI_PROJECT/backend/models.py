from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    reviews = relationship("CodeReview", back_populates="owner")

class CodeReview(Base):
    __tablename__ = "code_reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    language = Column(String, nullable=False) # e.g., "python", "java"
    original_code = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="reviews")
    analysis = relationship("AnalysisResult", back_populates="review", uselist=False)

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("code_reviews.id"))
    
    # AI generated fields
    general_explanation = Column(Text, nullable=False)
    time_complexity_original = Column(String, nullable=False)
    line_by_line_explanation = Column(Text, nullable=False) # JSON encoded string
    
    optimized_code = Column(Text, nullable=True)
    time_complexity_optimized = Column(String, nullable=True)
    optimization_explanation = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    review = relationship("CodeReview", back_populates="analysis")


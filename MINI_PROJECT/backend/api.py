import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models, schemas
from auth import get_current_user
from ai_service import analyze_code_with_ai

router = APIRouter()

@router.post("/analyze-code", response_model=schemas.CodeReviewResponse)
def analyze_code(
    request: schemas.CodeReviewRequest, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    try:
        # Generate the analysis using the Hugging Face AI pipeline
        ai_response = analyze_code_with_ai(request.code, request.language)
        
        # Save the review in the database
        new_review = models.CodeReview(
            user_id=current_user.id,
            language=request.language,
            original_code=request.code
        )
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
        
        # Save the analysis result in the database
        new_analysis = models.AnalysisResult(
            review_id=new_review.id,
            general_explanation=ai_response["general_explanation"],
            time_complexity_original=ai_response["time_complexity_original"],
            line_by_line_explanation=ai_response["line_by_line_explanation"],
            optimized_code=ai_response["optimized_code"],
            time_complexity_optimized=ai_response["time_complexity_optimized"],
            optimization_explanation=ai_response["optimization_explanation"]
        )
        db.add(new_analysis)
        db.commit()
        db.refresh(new_analysis)
        
        # Return response matching the schema
        return schemas.CodeReviewResponse(
            id=new_review.id,
            language=new_review.language,
            original_code=new_review.original_code,
            created_at=new_review.created_at,
            analysis=schemas.CodeAnalysisResponse(**ai_response)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )

@router.get("/history", response_model=List[schemas.CodeReviewResponse])
def get_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    from sqlalchemy.orm import selectinload
    
    reviews = db.query(models.CodeReview).options(selectinload(models.CodeReview.analysis)).filter(models.CodeReview.user_id == current_user.id).all()
    return reviews

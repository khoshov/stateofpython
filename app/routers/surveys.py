from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.models.models import Survey, QuestionCategory
from app.schemas.schemas import Survey as SurveySchema, SurveyCreate, QuestionCategory as QuestionCategorySchema, QuestionCategoryCreate

router = APIRouter()


@router.post("/", response_model=SurveySchema)
def create_survey(survey: SurveyCreate, db: Session = Depends(get_db)):
    db_survey = Survey(**survey.dict())
    db.add(db_survey)
    db.commit()
    db.refresh(db_survey)
    return db_survey


@router.get("/{survey_id}", response_model=SurveySchema)
def get_survey(survey_id: UUID, db: Session = Depends(get_db)):
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    return survey


@router.get("/", response_model=List[SurveySchema])
def get_surveys(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    surveys = db.query(Survey).offset(skip).limit(limit).all()
    return surveys


@router.post("/categories/", response_model=QuestionCategorySchema)
def create_question_category(category: QuestionCategoryCreate, db: Session = Depends(get_db)):
    db_category = QuestionCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.get("/categories/", response_model=List[QuestionCategorySchema])
def get_question_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = db.query(QuestionCategory).offset(skip).limit(limit).all()
    return categories


@router.get("/categories/{category_id}", response_model=QuestionCategorySchema)
def get_question_category(category_id: UUID, db: Session = Depends(get_db)):
    category = db.query(QuestionCategory).filter(QuestionCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Question category not found")
    return category
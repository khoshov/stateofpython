from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.models.models import Question, Option, Survey, QuestionCategory
from app.schemas.schemas import Question as QuestionSchema, QuestionCreate, Option as OptionSchema, OptionCreate

router = APIRouter()


@router.post("/", response_model=QuestionSchema)
def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    # Проверяем, что опрос существует
    survey = db.query(Survey).filter(Survey.id == question.survey_id).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    
    # Проверяем, что категория существует
    category = db.query(QuestionCategory).filter(QuestionCategory.id == question.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Question category not found")
    
    db_question = Question(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


@router.get("/{question_id}", response_model=QuestionSchema)
def get_question(question_id: UUID, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@router.get("/", response_model=List[QuestionSchema])
def get_questions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    questions = db.query(Question).offset(skip).limit(limit).all()
    return questions


@router.get("/survey/{survey_id}", response_model=List[QuestionSchema])
def get_questions_by_survey(survey_id: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    questions = db.query(Question).filter(Question.survey_id == survey_id).offset(skip).limit(limit).all()
    return questions


@router.post("/{question_id}/options", response_model=OptionSchema)
def create_option(question_id: UUID, option: OptionCreate, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    db_option = Option(question_id=question_id, **option.dict(exclude={'question_id'}))
    db.add(db_option)
    db.commit()
    db.refresh(db_option)
    return db_option


@router.get("/{question_id}/options", response_model=List[OptionSchema])
def get_question_options(question_id: UUID, db: Session = Depends(get_db)):
    options = db.query(Option).filter(Option.question_id == question_id).all()
    return options
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.models.models import Answer, AnswerOption, User, Question, Option
from app.schemas.schemas import Answer as AnswerSchema, AnswerCreate, AnswerOption as AnswerOptionSchema, AnswerOptionCreate

router = APIRouter()


@router.post("/", response_model=AnswerSchema)
def create_answer(answer: AnswerCreate, db: Session = Depends(get_db)):
    # Проверяем, что пользователь существует
    user = db.query(User).filter(User.id == answer.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Проверяем, что вопрос существует
    question = db.query(Question).filter(Question.id == answer.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    db_answer = Answer(**answer.dict())
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


@router.get("/{answer_id}", response_model=AnswerSchema)
def get_answer(answer_id: UUID, db: Session = Depends(get_db)):
    answer = db.query(Answer).filter(Answer.id == answer_id).first()
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    return answer


@router.get("/", response_model=List[AnswerSchema])
def get_answers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    answers = db.query(Answer).offset(skip).limit(limit).all()
    return answers


@router.get("/user/{user_id}", response_model=List[AnswerSchema])
def get_user_answers(user_id: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    answers = db.query(Answer).filter(Answer.user_id == user_id).offset(skip).limit(limit).all()
    return answers


@router.post("/{answer_id}/options", response_model=AnswerOptionSchema)
def create_answer_option(answer_id: UUID, answer_option: AnswerOptionCreate, db: Session = Depends(get_db)):
    answer = db.query(Answer).filter(Answer.id == answer_id).first()
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    
    # Проверяем, что вариант ответа существует
    option = db.query(Option).filter(Option.id == answer_option.option_id).first()
    if not option:
        raise HTTPException(status_code=404, detail="Option not found")
    
    db_answer_option = AnswerOption(answer_id=answer_id, **answer_option.dict(exclude={'answer_id'}))
    db.add(db_answer_option)
    db.commit()
    db.refresh(db_answer_option)
    return db_answer_option


@router.get("/{answer_id}/options", response_model=List[AnswerOptionSchema])
def get_answer_options(answer_id: UUID, db: Session = Depends(get_db)):
    options = db.query(AnswerOption).filter(AnswerOption.answer_id == answer_id).all()
    return options
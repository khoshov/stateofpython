from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
import uuid
import secrets
from datetime import datetime

from app.core.database import get_db
from app.models.models import User, Survey, Question, Answer, Option, AnswerOption
from app.schemas.schemas import User as UserSchema, Survey as SurveySchema, Question as QuestionSchema, Answer as AnswerSchema, Option as OptionSchema
from app.services.email_service import email_service
from pydantic import BaseModel, EmailStr

router = APIRouter()

# Request/Response models for survey API
class ParticipateRequest(BaseModel):
    email: EmailStr
    survey_id: Optional[str] = None  # Will use first available survey if not specified

class ParticipateResponse(BaseModel):
    token: str
    message: str

class QuestionWithOptions(BaseModel):
    id: str
    text: str
    type: str
    is_required: bool
    order_index: int
    options: Optional[List[OptionSchema]] = None

class SubmitAnswerRequest(BaseModel):
    token: str
    question_id: str
    text_answer: Optional[str] = None
    number_answer: Optional[int] = None
    boolean_answer: Optional[bool] = None
    selected_option_ids: Optional[List[str]] = None

class SubmitAnswerResponse(BaseModel):
    success: bool
    message: str

class UserAnswerResult(BaseModel):
    question_id: str
    question_text: str
    question_type: str
    text_answer: Optional[str] = None
    number_answer: Optional[int] = None
    boolean_answer: Optional[bool] = None
    selected_options: Optional[List[str]] = None

class SurveyResults(BaseModel):
    user_email: str
    survey_title: str
    completed_at: Optional[str] = None
    answers: List[UserAnswerResult]

# In-memory token storage (replace with Redis or database in production)
survey_tokens = {}

@router.post("/participate", response_model=ParticipateResponse)
async def participate_in_survey(
    request: ParticipateRequest,
    db: Session = Depends(get_db)
):
    """Submit email to participate in survey and get token"""
    
    # Get survey - use provided ID or first available survey
    survey = None
    if request.survey_id:
        try:
            survey = db.query(Survey).filter(Survey.id == uuid.UUID(request.survey_id)).first()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid survey ID format")
    else:
        # Get first available survey
        survey = db.query(Survey).first()
    
    if not survey:
        raise HTTPException(status_code=404, detail="No surveys available")
    
    # Create or get user
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        user = User(email=request.email)
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Generate unique token
    token = secrets.token_urlsafe(32)
    
    # Store token mapping (in production, use Redis or database)
    survey_tokens[token] = {
        "user_id": str(user.id),
        "survey_id": str(survey.id),
        "created_at": datetime.now(),
        "current_question_index": 0
    }
    
    # Send email invitation
    email_sent = await email_service.send_survey_invitation(
        email=request.email,
        token=token,
        survey_title=survey.title,
        survey_description=survey.description or ""
    )
    
    if email_sent:
        return ParticipateResponse(
            token=token,
            message="Survey invitation sent to your email. Please check your inbox and follow the link."
        )
    else:
        # If email fails, still return token for development
        return ParticipateResponse(
            token=token,
            message="Survey link generated. Email service unavailable - use this token: " + token
        )

@router.get("/questions", response_model=List[QuestionWithOptions])
def get_survey_questions(
    token: str,
    db: Session = Depends(get_db)
):
    """Get questions for a survey session"""
    
    if token not in survey_tokens:
        raise HTTPException(status_code=404, detail="Invalid or expired token")
    
    session_data = survey_tokens[token]
    survey_id = uuid.UUID(session_data["survey_id"])
    
    # Get questions for the survey
    questions = db.query(Question).filter(
        Question.survey_id == survey_id
    ).order_by(Question.order).all()
    
    # Get options for each question
    result = []
    for question in questions:
        options = db.query(Option).filter(
            Option.question_id == question.id
        ).order_by(Option.order).all()
        
        question_data = QuestionWithOptions(
            id=str(question.id),
            text=question.text,
            type=question.type,
            is_required=question.is_required,
            order_index=question.order,
            options=[OptionSchema.model_validate(opt) for opt in options] if options else None
        )
        result.append(question_data)
    
    return result

@router.post("/answer", response_model=SubmitAnswerResponse)
def submit_answer(
    request: SubmitAnswerRequest,
    db: Session = Depends(get_db)
):
    """Submit an answer for a question"""
    
    if request.token not in survey_tokens:
        raise HTTPException(status_code=404, detail="Invalid or expired token")
    
    session_data = survey_tokens[request.token]
    user_id = uuid.UUID(session_data["user_id"])
    question_id = uuid.UUID(request.question_id)
    
    # Check if question exists
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Delete existing answer for this question (allow updates)
    existing_answer = db.query(Answer).filter(
        and_(Answer.user_id == user_id, Answer.question_id == question_id)
    ).first()
    
    if existing_answer:
        # Delete existing answer options
        db.query(AnswerOption).filter(AnswerOption.answer_id == existing_answer.id).delete()
        db.delete(existing_answer)
        db.commit()
    
    # Create new answer
    answer = Answer(
        user_id=user_id,
        question_id=question_id,
        text_answer=request.text_answer,
        number_answer=request.number_answer,
        boolean_answer=request.boolean_answer
    )
    db.add(answer)
    db.commit()
    db.refresh(answer)
    
    # Add selected options if any
    if request.selected_option_ids:
        for option_id_str in request.selected_option_ids:
            option_id = uuid.UUID(option_id_str)
            # Verify option exists and belongs to the question
            option = db.query(Option).filter(
                and_(Option.id == option_id, Option.question_id == question_id)
            ).first()
            
            if option:
                answer_option = AnswerOption(
                    answer_id=answer.id,
                    option_id=option_id
                )
                db.add(answer_option)
        
        db.commit()
    
    return SubmitAnswerResponse(
        success=True,
        message="Answer submitted successfully"
    )

@router.get("/results", response_model=SurveyResults)
def get_survey_results(
    token: str,
    db: Session = Depends(get_db)
):
    """Get user's survey results"""
    
    if token not in survey_tokens:
        raise HTTPException(status_code=404, detail="Invalid or expired token")
    
    session_data = survey_tokens[token]
    user_id = uuid.UUID(session_data["user_id"])
    survey_id = uuid.UUID(session_data["survey_id"])
    
    # Get user and survey info
    user = db.query(User).filter(User.id == user_id).first()
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    
    if not user or not survey:
        raise HTTPException(status_code=404, detail="User or survey not found")
    
    # Get all answers by this user for this survey
    answers = db.query(Answer).join(Question).filter(
        and_(
            Answer.user_id == user_id,
            Question.survey_id == survey_id
        )
    ).all()
    
    # Format results
    answer_results = []
    for answer in answers:
        question = answer.question
        
        # Get selected options for this answer
        selected_options = []
        answer_options = db.query(AnswerOption).join(Option).filter(
            AnswerOption.answer_id == answer.id
        ).all()
        
        for answer_option in answer_options:
            selected_options.append(answer_option.option.text)
        
        answer_result = UserAnswerResult(
            question_id=str(question.id),
            question_text=question.text,
            question_type=question.type,
            text_answer=answer.text_answer,
            number_answer=answer.number_answer,
            boolean_answer=answer.boolean_answer,
            selected_options=selected_options if selected_options else None
        )
        answer_results.append(answer_result)
    
    # Sort by question order
    questions_order = {str(q.id): q.order for q in db.query(Question).filter(Question.survey_id == survey_id).all()}
    answer_results.sort(key=lambda x: questions_order.get(x.question_id, 0))
    
    return SurveyResults(
        user_email=user.email,
        survey_title=survey.title,
        completed_at=datetime.now().isoformat() if answer_results else None,
        answers=answer_results
    )

@router.get("/surveys", response_model=List[dict])
def get_available_surveys(db: Session = Depends(get_db)):
    """Get list of available surveys"""
    
    surveys = db.query(Survey).all()
    
    return [
        {
            "id": str(survey.id),
            "title": survey.title,
            "description": survey.description,
            "created_at": survey.created_at.isoformat(),
            "question_count": db.query(Question).filter(Question.survey_id == survey.id).count()
        }
        for survey in surveys
    ]

@router.get("/survey/{survey_id}", response_model=dict) 
def get_survey_details(survey_id: str, db: Session = Depends(get_db)):
    """Get details of a specific survey"""
    
    try:
        survey_uuid = uuid.UUID(survey_id)
        survey = db.query(Survey).filter(Survey.id == survey_uuid).first()
        
        if not survey:
            raise HTTPException(status_code=404, detail="Survey not found")
        
        questions = db.query(Question).filter(Question.survey_id == survey_uuid).order_by(Question.order).all()
        
        return {
            "id": str(survey.id),
            "title": survey.title,
            "description": survey.description,
            "created_at": survey.created_at.isoformat(),
            "questions": [
                {
                    "id": str(q.id),
                    "text": q.text,
                    "type": q.type,
                    "is_required": q.is_required,
                    "order": q.order,
                    "options": [
                        {
                            "id": str(opt.id),
                            "text": opt.text,
                            "order": opt.order
                        }
                        for opt in db.query(Option).filter(Option.question_id == q.id).order_by(Option.order).all()
                    ]
                }
                for q in questions
            ]
        }
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid survey ID format")

@router.post("/complete", response_model=SubmitAnswerResponse)
def complete_survey(
    request: dict,  # {"token": "..."}
    db: Session = Depends(get_db)
):
    """Mark survey as completed"""
    
    token = request.get("token")
    if not token or token not in survey_tokens:
        raise HTTPException(status_code=404, detail="Invalid or expired token")
    
    # In a real implementation, you might want to:
    # 1. Mark the survey session as completed
    # 2. Send notification email
    # 3. Update analytics
    
    return SubmitAnswerResponse(
        success=True,
        message="Survey completed successfully"
    )
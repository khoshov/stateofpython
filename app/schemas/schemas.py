from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserProfileBase(BaseModel):
    full_name: Optional[str] = None
    gender: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    age: Optional[int] = None


class UserProfileCreate(UserProfileBase):
    pass


class UserProfile(UserProfileBase):
    user_id: UUID
    
    class Config:
        from_attributes = True


class SurveyBase(BaseModel):
    title: str
    description: Optional[str] = None


class SurveyCreate(SurveyBase):
    pass


class Survey(SurveyBase):
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


class QuestionCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


class QuestionCategoryCreate(QuestionCategoryBase):
    pass


class QuestionCategory(QuestionCategoryBase):
    id: UUID
    
    class Config:
        from_attributes = True


class QuestionBase(BaseModel):
    text: str
    description: Optional[str] = None
    type: str
    order: int


class QuestionCreate(QuestionBase):
    survey_id: UUID
    category_id: UUID


class Question(QuestionBase):
    id: UUID
    survey_id: UUID
    category_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


class OptionBase(BaseModel):
    text: str
    order: int


class OptionCreate(OptionBase):
    question_id: UUID


class Option(OptionBase):
    id: UUID
    question_id: UUID
    
    class Config:
        from_attributes = True


class AnswerBase(BaseModel):
    pass


class AnswerCreate(AnswerBase):
    user_id: UUID
    question_id: UUID


class Answer(AnswerBase):
    id: UUID
    user_id: UUID
    question_id: UUID
    answered_at: datetime
    
    class Config:
        from_attributes = True


class AnswerOptionBase(BaseModel):
    pass


class AnswerOptionCreate(AnswerOptionBase):
    answer_id: UUID
    option_id: UUID


class AnswerOption(AnswerOptionBase):
    id: UUID
    answer_id: UUID
    option_id: UUID
    
    class Config:
        from_attributes = True


class NotificationBase(BaseModel):
    message: str
    read: bool = False


class NotificationCreate(NotificationBase):
    user_id: UUID


class Notification(NotificationBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True
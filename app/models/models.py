from sqlalchemy import Column, String, Integer, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import hashlib

from app.core.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    answers = relationship("Answer", back_populates="user")
    notifications = relationship("Notification", back_populates="user")


class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    full_name = Column(Text)
    gender = Column(Text)
    city = Column(Text)
    country = Column(Text)
    age = Column(Integer)
    
    user = relationship("User", back_populates="profile")


class Survey(Base):
    __tablename__ = "surveys"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(Text, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    questions = relationship("Question", back_populates="survey")


class QuestionCategory(Base):
    __tablename__ = "question_categories"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)
    description = Column(Text)
    
    questions = relationship("Question", back_populates="category")


class Question(Base):
    __tablename__ = "questions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    survey_id = Column(UUID(as_uuid=True), ForeignKey("surveys.id"))
    category_id = Column(UUID(as_uuid=True), ForeignKey("question_categories.id"), nullable=True)
    text = Column(Text, nullable=False)
    description = Column(Text)
    type = Column(Text, nullable=False)
    is_required = Column(Boolean, default=False)
    order = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    survey = relationship("Survey", back_populates="questions")
    category = relationship("QuestionCategory", back_populates="questions")
    options = relationship("Option", back_populates="question")
    answers = relationship("Answer", back_populates="question")


class Option(Base):
    __tablename__ = "options"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"))
    text = Column(Text, nullable=False)
    order = Column(Integer, nullable=False)
    
    question = relationship("Question", back_populates="options")
    answer_options = relationship("AnswerOption", back_populates="option")


class Answer(Base):
    __tablename__ = "answers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"))
    text_answer = Column(Text, nullable=True)
    number_answer = Column(Integer, nullable=True)
    boolean_answer = Column(Boolean, nullable=True)
    answered_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="answers")
    question = relationship("Question", back_populates="answers")
    answer_options = relationship("AnswerOption", back_populates="answer")


class AnswerOption(Base):
    __tablename__ = "answer_options"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    answer_id = Column(UUID(as_uuid=True), ForeignKey("answers.id"))
    option_id = Column(UUID(as_uuid=True), ForeignKey("options.id"))
    
    answer = relationship("Answer", back_populates="answer_options")
    option = relationship("Option", back_populates="answer_options")


class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    message = Column(Text, nullable=False)
    read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="notifications")


class AdminUser(Base):
    __tablename__ = "admin_users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str) -> bool:
        """Verify password against hash"""
        return self.password_hash == self.hash_password(password)
    
    @classmethod
    def create_admin(cls, username: str, email: str, password: str, is_superuser: bool = False):
        """Create new admin user"""
        return cls(
            username=username,
            email=email,
            password_hash=cls.hash_password(password),
            is_superuser=is_superuser
        )
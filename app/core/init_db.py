import asyncio
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.models import Base, User, UserProfile, Survey, QuestionCategory, Question, Option
import uuid


def init_db():
    """Инициализация базы данных с примерами данных"""
    
    # Создание всех таблиц
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Проверяем, есть ли уже данные
        if db.query(User).first():
            print("База данных уже инициализирована")
            return
        
        # Создание пользователя
        user = User(
            id=uuid.uuid4(),
            email="test@example.com",
            username="testuser"
        )
        db.add(user)
        db.flush()
        
        # Создание профиля пользователя
        profile = UserProfile(
            user_id=user.id,
            full_name="Test User",
            gender="male",
            city="Moscow",
            country="Russia",
            age=30
        )
        db.add(profile)
        
        # Создание опроса
        survey = Survey(
            id=uuid.uuid4(),
            title="State of Python 2025",
            description="Опрос о состоянии Python экосистемы в 2025 году"
        )
        db.add(survey)
        db.flush()
        
        # Создание категории вопросов
        category = QuestionCategory(
            id=uuid.uuid4(),
            name="Python Usage",
            description="Вопросы об использовании Python"
        )
        db.add(category)
        db.flush()
        
        # Создание вопросов
        question1 = Question(
            id=uuid.uuid4(),
            survey_id=survey.id,
            category_id=category.id,
            text="Какую версию Python вы используете?",
            description="Выберите основную версию Python в ваших проектах",
            type="single_choice",
            is_required=True,
            order=1
        )
        db.add(question1)
        db.flush()
        
        question2 = Question(
            id=uuid.uuid4(),
            survey_id=survey.id,
            category_id=category.id,
            text="Какие фреймворки вы используете?",
            description="Выберите все подходящие варианты",
            type="multiple_choice",
            is_required=False,
            order=2
        )
        db.add(question2)
        db.flush()
        
        # Добавим текстовый вопрос
        question3 = Question(
            id=uuid.uuid4(),
            survey_id=survey.id,
            category_id=category.id,
            text="Расскажите о своем опыте с Python",
            description="Поделитесь своим опытом использования Python",
            type="text",
            is_required=False,
            order=3
        )
        db.add(question3)
        db.flush()
        
        # Добавим числовой вопрос
        question4 = Question(
            id=uuid.uuid4(),
            survey_id=survey.id,
            category_id=category.id,
            text="Сколько лет вы программируете на Python?",
            description="Укажите количество лет",
            type="number",
            is_required=True,
            order=4
        )
        db.add(question4)
        db.flush()
        
        # Создание вариантов ответов для первого вопроса
        options_q1 = [
            Option(id=uuid.uuid4(), question_id=question1.id, text="Python 3.9", order=1),
            Option(id=uuid.uuid4(), question_id=question1.id, text="Python 3.10", order=2),
            Option(id=uuid.uuid4(), question_id=question1.id, text="Python 3.11", order=3),
            Option(id=uuid.uuid4(), question_id=question1.id, text="Python 3.12", order=4),
            Option(id=uuid.uuid4(), question_id=question1.id, text="Python 3.13", order=5),
        ]
        
        # Создание вариантов ответов для второго вопроса
        options_q2 = [
            Option(id=uuid.uuid4(), question_id=question2.id, text="Django", order=1),
            Option(id=uuid.uuid4(), question_id=question2.id, text="FastAPI", order=2),
            Option(id=uuid.uuid4(), question_id=question2.id, text="Flask", order=3),
            Option(id=uuid.uuid4(), question_id=question2.id, text="Tornado", order=4),
            Option(id=uuid.uuid4(), question_id=question2.id, text="Starlette", order=5),
        ]
        
        db.add_all(options_q1 + options_q2)
        
        db.commit()
        print("База данных успешно инициализирована с примерами данных")
        
    except Exception as e:
        db.rollback()
        print(f"Ошибка при инициализации базы данных: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
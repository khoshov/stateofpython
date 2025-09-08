#!/usr/bin/env python3
"""
Создание дополнительных тестовых данных для демонстрации админки
"""

from app.core.database import SessionLocal
from app.models.models import User, UserProfile, Survey, QuestionCategory, Question, Option, Answer, AnswerOption, Notification
import uuid

def create_test_data():
    """Создание дополнительных тестовых данных"""
    
    db = SessionLocal()
    
    try:
        # Создаем несколько пользователей
        users_data = [
            {"email": "alice@example.com", "username": "alice"},
            {"email": "bob@example.com", "username": "bob"},
            {"email": "charlie@example.com", "username": "charlie"},
            {"email": "diana@example.com", "username": "diana"},
        ]
        
        created_users = []
        for user_data in users_data:
            # Проверим, не существует ли уже такой пользователь
            existing = db.query(User).filter(User.email == user_data["email"]).first()
            if not existing:
                user = User(
                    id=uuid.uuid4(),
                    email=user_data["email"],
                    username=user_data["username"]
                )
                db.add(user)
                db.flush()
                created_users.append(user)
                
                # Создаем профиль для каждого пользователя
                profiles_data = {
                    "alice@example.com": {"full_name": "Alice Johnson", "gender": "female", "city": "New York", "country": "USA", "age": 28},
                    "bob@example.com": {"full_name": "Bob Smith", "gender": "male", "city": "London", "country": "UK", "age": 34},
                    "charlie@example.com": {"full_name": "Charlie Brown", "gender": "male", "city": "Berlin", "country": "Germany", "age": 25},
                    "diana@example.com": {"full_name": "Diana Prince", "gender": "female", "city": "Paris", "country": "France", "age": 31},
                }
                
                if user.email in profiles_data:
                    profile_data = profiles_data[user.email]
                    profile = UserProfile(
                        user_id=user.id,
                        **profile_data
                    )
                    db.add(profile)
        
        # Создаем дополнительный опрос
        existing_survey = db.query(Survey).filter(Survey.title == "JavaScript Ecosystem 2025").first()
        if not existing_survey:
            js_survey = Survey(
                id=uuid.uuid4(),
                title="JavaScript Ecosystem 2025",
                description="Опрос о состоянии JavaScript экосистемы"
            )
            db.add(js_survey)
            db.flush()
            
            # Создаем категорию для JS вопросов
            js_category = QuestionCategory(
                id=uuid.uuid4(),
                name="JavaScript Tools",
                description="Вопросы об инструментах JavaScript"
            )
            db.add(js_category)
            db.flush()
            
            # Добавляем вопросы для JS опроса
            js_questions = [
                {
                    "text": "Какой фреймворк вы предпочитаете для фронтенда?",
                    "type": "single_choice",
                    "is_required": True,
                    "order": 1,
                    "options": ["React", "Vue.js", "Angular", "Svelte", "Solid.js"]
                },
                {
                    "text": "Какие инструменты сборки вы используете?",
                    "type": "multiple_choice", 
                    "is_required": False,
                    "order": 2,
                    "options": ["Webpack", "Vite", "Rollup", "Parcel", "ESBuild", "Turbopack"]
                },
                {
                    "text": "Оцените уровень удовлетворенности JavaScript (1-10)",
                    "type": "number",
                    "is_required": True,
                    "order": 3,
                    "options": []
                },
                {
                    "text": "Что вам больше всего нравится в современном JavaScript?",
                    "type": "text",
                    "is_required": False,
                    "order": 4,
                    "options": []
                }
            ]
            
            for q_data in js_questions:
                question = Question(
                    id=uuid.uuid4(),
                    survey_id=js_survey.id,
                    category_id=js_category.id,
                    text=q_data["text"],
                    type=q_data["type"],
                    is_required=q_data["is_required"],
                    order=q_data["order"]
                )
                db.add(question)
                db.flush()
                
                # Добавляем опции если есть
                for i, option_text in enumerate(q_data["options"], 1):
                    option = Option(
                        id=uuid.uuid4(),
                        question_id=question.id,
                        text=option_text,
                        order=i
                    )
                    db.add(option)
        
        # Создаем уведомления для пользователей
        if created_users:
            notifications_data = [
                "Добро пожаловать в Survey API!",
                "Не забудьте пройти новый опрос о JavaScript",
                "Результаты опроса о Python уже доступны",
                "Обновление системы запланировано на завтра"
            ]
            
            for i, user in enumerate(created_users[:2]):  # Только для первых двух пользователей
                for j, message in enumerate(notifications_data[:2]):  # Только первые два сообщения
                    notification = Notification(
                        id=uuid.uuid4(),
                        user_id=user.id,
                        message=f"{message} (пользователь: {user.username})",
                        read=j == 0  # Первое уведомление прочитано, второе - нет
                    )
                    db.add(notification)
        
        db.commit()
        print("✅ Тестовые данные успешно созданы!")
        
        # Показываем статистику
        print("\n📊 Статистика данных:")
        print(f"Пользователи: {db.query(User).count()}")
        print(f"Профили: {db.query(UserProfile).count()}")
        print(f"Опросы: {db.query(Survey).count()}")
        print(f"Категории: {db.query(QuestionCategory).count()}")
        print(f"Вопросы: {db.query(Question).count()}")
        print(f"Варианты ответов: {db.query(Option).count()}")
        print(f"Ответы: {db.query(Answer).count()}")
        print(f"Уведомления: {db.query(Notification).count()}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка создания тестовых данных: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data()
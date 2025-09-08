from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.middleware.sessions import SessionMiddleware
from app.core.database import engine
from app.models.models import Base
from app.routers import users, surveys, questions, answers, notifications, survey_api
from app.core.init_db import init_db
from app.admin import setup_admin

Base.metadata.create_all(bind=engine)

# Инициализация базы данных с примерами данных
try:
    init_db()
except Exception as e:
    print(f"Предупреждение: Не удалось инициализировать базу данных: {e}")

app = FastAPI(
    title="Survey API",
    description="API для системы опросов, клон survey.devographics.com",
    version="1.0.0"
)

# Add session middleware for admin authentication
app.add_middleware(
    SessionMiddleware, 
    secret_key="your-secret-key-change-in-production"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение статических файлов
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(surveys.router, prefix="/api/v1/surveys", tags=["surveys"])
app.include_router(questions.router, prefix="/api/v1/questions", tags=["questions"])
app.include_router(answers.router, prefix="/api/v1/answers", tags=["answers"])
app.include_router(notifications.router, prefix="/api/v1/notifications", tags=["notifications"])
app.include_router(survey_api.router, prefix="/api/v1/survey", tags=["survey-api"])

# Setup SQLAdmin
admin = setup_admin(app, engine)


@app.get("/")
async def root():
    return FileResponse("app/static/index.html")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
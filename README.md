# Survey API

FastAPI проект для создания системы опросов, вдохновленный survey.devographics.com.

## Особенности

- FastAPI для REST API
- SQLAlchemy для работы с базой данных
- PostgreSQL как основная база данных
- Pydantic для валидации данных
- Alembic для миграций базы данных

## Структура проекта

```
app/
├── core/
│   ├── config.py       # Конфигурация приложения
│   └── database.py     # Настройки базы данных
├── models/
│   └── models.py       # SQLAlchemy модели
├── schemas/
│   └── schemas.py      # Pydantic схемы
├── routers/
│   ├── users.py        # Роуты для пользователей
│   ├── surveys.py      # Роуты для опросов
│   ├── questions.py    # Роуты для вопросов
│   ├── answers.py      # Роуты для ответов
│   └── notifications.py # Роуты для уведомлений
└── main.py            # Основное приложение
```

## Установка

### С Docker (рекомендуется)

1. Клонируйте репозиторий
2. Запустите проект:
   ```bash
   docker-compose up -d
   ```

Это запустит:
- API на порту 8000
- PostgreSQL на порту 5432
- Adminer (веб-интерфейс для БД) на порту 8080

### С UV (локальная разработка)

1. Клонируйте репозиторий
2. Установите зависимости:
   ```bash
   uv sync
   ```

3. Создайте файл `.env` на основе `.env.example` и настройте переменные окружения

4. Запустите приложение:
   ```bash
   uv run uvicorn app.main:app --reload
   ```

### Альтернативный способ с pip

1. Клонируйте репозиторий
2. Создайте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # или
   venv\Scripts\activate     # Windows
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Создайте файл `.env` на основе `.env.example` и настройте переменные окружения

5. Запустите приложение:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

### Пользователи
- `POST /api/v1/users/` - Создать пользователя
- `GET /api/v1/users/{user_id}` - Получить пользователя
- `GET /api/v1/users/` - Получить список пользователей
- `POST /api/v1/users/{user_id}/profile` - Создать профиль пользователя
- `GET /api/v1/users/{user_id}/profile` - Получить профиль пользователя

### Опросы
- `POST /api/v1/surveys/` - Создать опрос
- `GET /api/v1/surveys/{survey_id}` - Получить опрос
- `GET /api/v1/surveys/` - Получить список опросов
- `POST /api/v1/surveys/categories/` - Создать категорию вопросов
- `GET /api/v1/surveys/categories/` - Получить список категорий

### Вопросы
- `POST /api/v1/questions/` - Создать вопрос
- `GET /api/v1/questions/{question_id}` - Получить вопрос
- `GET /api/v1/questions/` - Получить список вопросов
- `GET /api/v1/questions/survey/{survey_id}` - Получить вопросы опроса
- `POST /api/v1/questions/{question_id}/options` - Создать вариант ответа
- `GET /api/v1/questions/{question_id}/options` - Получить варианты ответов

### Ответы
- `POST /api/v1/answers/` - Создать ответ
- `GET /api/v1/answers/{answer_id}` - Получить ответ
- `GET /api/v1/answers/` - Получить список ответов
- `GET /api/v1/answers/user/{user_id}` - Получить ответы пользователя
- `POST /api/v1/answers/{answer_id}/options` - Добавить выбранный вариант
- `GET /api/v1/answers/{answer_id}/options` - Получить выбранные варианты

### Уведомления
- `POST /api/v1/notifications/` - Создать уведомление
- `GET /api/v1/notifications/{notification_id}` - Получить уведомление
- `GET /api/v1/notifications/user/{user_id}` - Получить уведомления пользователя
- `PATCH /api/v1/notifications/{notification_id}/read` - Отметить как прочитанное

## База данных

Проект использует PostgreSQL. Схема базы данных включает следующие таблицы:

- `users` - Пользователи
- `user_profiles` - Профили пользователей
- `surveys` - Опросы
- `question_categories` - Категории вопросов
- `questions` - Вопросы
- `options` - Варианты ответов
- `answers` - Ответы пользователей
- `answer_options` - Выбранные варианты ответов
- `notifications` - Уведомления

## Docker команды

### Основные команды

```bash
# Запуск всех сервисов
docker-compose up -d

# Остановка всех сервисов
docker-compose down

# Просмотр логов
docker-compose logs -f

# Перезапуск API
docker-compose restart api

# Сборка с обновлением
docker-compose up --build -d
```

### Управление базой данных

```bash
# Подключение к PostgreSQL
docker-compose exec db psql -U survey_user -d survey_db

# Создание миграций
docker-compose exec api uv run alembic revision --autogenerate -m "Initial migration"

# Применение миграций
docker-compose exec api uv run alembic upgrade head
```

## Разработка

### С Docker

Для разработки с Docker используйте:

```bash
docker-compose up -d
```

### С UV (локально)

Для разработки локально используйте:

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Линтинг и форматирование

```bash
# Форматирование кода
uv run black .

# Сортировка импортов
uv run isort .

# Проверка типов
uv run mypy .

# Проверка кода
uv run flake8 .
```

### Тестирование

```bash
uv run pytest
```

## Доступ к сервисам

После запуска `docker-compose up -d`:

- **API документация**: http://localhost:8000/docs
- **API**: http://localhost:8000
- **Adminer** (веб-интерфейс БД): http://localhost:8080
  - Сервер: `db`
  - Пользователь: `survey_user`
  - Пароль: `survey_pass`
  - База данных: `survey_db`
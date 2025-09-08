FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Создание рабочей директории
WORKDIR /app

# Копирование файлов зависимостей
COPY pyproject.toml uv.lock ./

# Установка зависимостей
RUN uv sync --no-dev

# Копирование исходного кода
COPY . .

# Создание пользователя без root прав
RUN useradd --create-home --shell /bin/bash app
USER app

# Открытие порта
EXPOSE 8000

# Команда запуска
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

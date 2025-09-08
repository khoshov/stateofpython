# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is "Survey API" - a full-stack survey system inspired by survey.devographics.com. The project consists of:
- **Backend**: FastAPI with SQLAlchemy, PostgreSQL for a comprehensive survey API
- **Frontend**: Next.js with shadcn/ui for a modern survey interface

## Development Commands

### Backend (FastAPI) - Package Management (UV - Primary)
```bash
# Install dependencies
uv sync

# Run the application
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Database migrations
uv run alembic revision --autogenerate -m "Migration message"
uv run alembic upgrade head

# Code quality tools
uv run black .          # Format code
uv run isort .          # Sort imports  
uv run mypy .           # Type checking
uv run flake8 .         # Linting
uv run pytest          # Run tests
```

### Docker Development (Recommended)
```bash
# Start all services (API, PostgreSQL, Adminer)
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Restart API only
docker-compose restart api

# Run migrations in container
docker-compose exec api uv run alembic upgrade head
```

### Backend Alternative (pip)
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend (Next.js)
```bash
cd frontend

# Install dependencies
npm install

# Setup environment
cp .env.local.example .env.local

# Run development server
npm run dev

# Build for production
npm run build
npm start
```

## Architecture

### Backend Structure
- **FastAPI Application**: Modern async web framework with automatic OpenAPI docs
- **SQLAlchemy ORM**: Database models with relationships for survey system
- **PostgreSQL**: Primary database with comprehensive survey schema
- **Pydantic**: Data validation and serialization schemas
- **Alembic**: Database migration management

### Frontend Structure
- **Next.js 15**: React framework with App Router
- **shadcn/ui**: Beautiful, accessible UI components built on Radix UI
- **Tailwind CSS**: Utility-first CSS framework
- **TypeScript**: Type-safe development

### Key Backend Components
- `app/main.py`: FastAPI application setup, middleware, and router registration
- `app/core/`: Configuration, database connection, and initialization
- `app/models/models.py`: SQLAlchemy database models (users, surveys, questions, answers, notifications)
- `app/schemas/schemas.py`: Pydantic schemas for API request/response validation
- `app/routers/`: API endpoints organized by domain (users, surveys, questions, answers, notifications)
- `app/routers/survey_api.py`: **NEW** Frontend-compatible survey API endpoints
- `app/admin.py`: **NEW** SQLAdmin configuration with Django-style admin interface

### Key Frontend Components
- `frontend/src/app/page.tsx`: Main landing page with email entry
- `frontend/src/app/survey/[token]/page.tsx`: Survey taking interface
- `frontend/src/app/results/[token]/page.tsx`: Results viewing page
- `frontend/src/components/ui/`: shadcn/ui component library
- `frontend/src/lib/api/`: API integration layer with type definitions

### Database Schema
The system models a complete survey platform:
- Users and user profiles
- Surveys with question categories
- Questions with multiple choice options
- User answers with selected options
- Notification system

### API Structure
- REST API with `/api/v1/` prefix
- Comprehensive CRUD operations for all entities
- **NEW** Frontend integration endpoints:
  - `POST /api/v1/survey/participate` - Submit email to participate
  - `GET /api/v1/survey/questions?token=` - Get survey questions
  - `POST /api/v1/survey/answer` - Submit question answer
  - `GET /api/v1/survey/results?token=` - Get user results
  - `POST /api/v1/survey/complete` - Mark survey complete
- Auto-generated documentation at `/docs`
- Health check endpoint at `/health`

## Development Notes

- Uses PostgreSQL as primary database (configured in docker-compose.yml)
- CORS enabled for all origins in development
- Static files served from `app/static/`
- Database initialization with sample data on startup
- Black formatter with 88 character line length
- Type checking with mypy enabled
- Python 3.11+ required

## Services Access (Docker)
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs  
- **Admin Panel**: http://localhost:8000/admin (username: `admin`, password: `admin`)
- **Frontend**: http://localhost:3000 (run separately)
- **PostgreSQL**: localhost:5432 (survey_user/survey_pass/survey_db)
- **Adminer**: http://localhost:8080

## User Flow Implementation

The frontend implements the complete user journey:
1. **Landing Page**: User enters email and clicks participate
2. **Email Processing**: Token generation and survey link (currently auto-redirects for demo)
3. **Survey Interface**: One question at a time with progress tracking
4. **Answer Submission**: Real-time saving after each question
5. **Results View**: Complete answer history and summary

## Full Stack Development

To run both backend and frontend:
```bash
# Terminal 1: Start backend with Docker
docker-compose up -d

# Terminal 2: Start frontend
cd frontend && npm run dev
```

The frontend at localhost:3000 will communicate with the FastAPI backend at localhost:8000.

## Admin Interface

### Features
- **Django-style admin panel** built with SQLAdmin
- **Complete CRUD operations** for all entities
- **User-friendly interface** with search, filtering, and pagination
- **Role-based access** with simple authentication
- **Data visualization** with icons and organized sections

### Admin Models
- **Users** - User account management with profiles
- **Surveys** - Survey creation and management  
- **Question Categories** - Organize questions by topics
- **Questions** - Question creation with different types (single/multiple choice, text, number)
- **Options** - Answer choices for selection questions
- **Answers** - User responses (read-only for data integrity)
- **Answer Options** - Selected answer choices (read-only)
- **Notifications** - User notification management

### Access
- URL: http://localhost:8000/admin
- Username: `admin`
- Password: `admin`
- **Note**: Change credentials in production by updating `app/admin.py`

### Usage Tips
- Use the **search bars** to quickly find records
- **Sort columns** by clicking headers  
- **Filter data** using the built-in filters
- **Bulk actions** available for selected records
- **Export/Import** functionality for data management
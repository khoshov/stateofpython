from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.core.database import SessionLocal
from app.models.models import User, UserProfile, Survey, QuestionCategory, Question, Option, Answer, AnswerOption, Notification, AdminUser


# Simple authentication backend for demo
class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        
        # Safely get form fields with error handling
        username = form.get("username")
        password = form.get("password")
        
        # Check if fields are present
        if not username or not password:
            return False
        
        # Database authentication
        db = SessionLocal()
        try:
            admin_user = db.query(AdminUser).filter(
                AdminUser.username == username,
                AdminUser.is_active == True
            ).first()
            
            if admin_user and admin_user.verify_password(password):
                # Update last login
                from datetime import datetime
                admin_user.last_login = datetime.now()
                db.commit()
                
                # Store user info in session
                request.session.update({
                    "admin_user_id": str(admin_user.id),
                    "username": admin_user.username,
                    "is_superuser": admin_user.is_superuser,
                    "authenticated": True
                })
                return True
            
            # Fallback to simple auth for backward compatibility
            if username == "admin" and password == "admin":
                request.session.update({"token": "authenticated"})
                return True
                
            return False
            
        except Exception as e:
            print(f"Login error: {e}")
            return False
        finally:
            db.close()

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        # Check modern authentication
        authenticated = request.session.get("authenticated")
        if authenticated:
            return True
            
        # Check legacy authentication for backward compatibility
        token = request.session.get("token")
        return token == "authenticated"


def setup_admin(app, engine):
    """Setup SQLAdmin with all model views"""
    
    authentication_backend = AdminAuth(secret_key="your-secret-key-change-in-production")
    
    admin = Admin(
        app, 
        engine, 
        authentication_backend=authentication_backend,
        title="Survey Admin",
        logo_url=None
    )
    
    # User Management
    class UserAdmin(ModelView, model=User):
        column_list = [User.id, User.email, User.username, User.created_at]
        column_searchable_list = [User.email, User.username]
        column_sortable_list = [User.email, User.created_at]
        column_details_exclude_list = [User.id]
        can_create = True
        can_edit = True
        can_delete = True
        name = "User"
        name_plural = "Users"
        icon = "fa-solid fa-user"
    
    class UserProfileAdmin(ModelView, model=UserProfile):
        column_list = [UserProfile.user_id, UserProfile.full_name, UserProfile.gender, 
                      UserProfile.city, UserProfile.country, UserProfile.age]
        column_searchable_list = [UserProfile.full_name, UserProfile.city, UserProfile.country]
        column_sortable_list = [UserProfile.full_name, UserProfile.age]
        can_create = True
        can_edit = True
        can_delete = True
        name = "User Profile"
        name_plural = "User Profiles"
        icon = "fa-solid fa-address-card"
    
    # Survey Management
    class SurveyAdmin(ModelView, model=Survey):
        column_list = [Survey.id, Survey.title, Survey.description, Survey.created_at]
        column_searchable_list = [Survey.title, Survey.description]
        column_sortable_list = [Survey.title, Survey.created_at]
        column_details_exclude_list = [Survey.id]
        can_create = True
        can_edit = True
        can_delete = True
        name = "Survey"
        name_plural = "Surveys"
        icon = "fa-solid fa-poll"
    
    class QuestionCategoryAdmin(ModelView, model=QuestionCategory):
        column_list = [QuestionCategory.id, QuestionCategory.name, QuestionCategory.description]
        column_searchable_list = [QuestionCategory.name, QuestionCategory.description]
        column_sortable_list = [QuestionCategory.name]
        column_details_exclude_list = [QuestionCategory.id]
        can_create = True
        can_edit = True
        can_delete = True
        name = "Question Category"
        name_plural = "Question Categories"
        icon = "fa-solid fa-tags"
    
    class QuestionAdmin(ModelView, model=Question):
        column_list = [Question.id, Question.text, Question.type, Question.is_required, 
                      Question.order, Question.survey_id, Question.category_id, Question.created_at]
        column_searchable_list = [Question.text, Question.description, Question.type]
        column_sortable_list = [Question.text, Question.type, Question.order, Question.created_at]
        column_details_exclude_list = [Question.id, Question.survey_id, Question.category_id]
        can_create = True
        can_edit = True
        can_delete = True
        name = "Question"
        name_plural = "Questions"
        icon = "fa-solid fa-question-circle"
        
        # Custom form configuration
        form_columns = [Question.survey_id, Question.category_id, Question.text, 
                       Question.description, Question.type, Question.is_required, Question.order]
    
    class OptionAdmin(ModelView, model=Option):
        column_list = [Option.id, Option.text, Option.order, Option.question_id]
        column_searchable_list = [Option.text]
        column_sortable_list = [Option.text, Option.order]
        column_details_exclude_list = [Option.id, Option.question_id]
        can_create = True
        can_edit = True
        can_delete = True
        name = "Option"
        name_plural = "Options"
        icon = "fa-solid fa-list-ul"
    
    # Answer Management
    class AnswerAdmin(ModelView, model=Answer):
        column_list = [Answer.id, Answer.user_id, Answer.question_id, Answer.text_answer,
                      Answer.number_answer, Answer.boolean_answer, Answer.answered_at]
        column_searchable_list = [Answer.text_answer]
        column_sortable_list = [Answer.answered_at]
        column_details_exclude_list = [Answer.id, Answer.user_id, Answer.question_id]
        can_create = True
        can_edit = True
        can_delete = True
        name = "Answer"
        name_plural = "Answers"
        icon = "fa-solid fa-reply"
        
        # Make it read-only by default to preserve data integrity
        can_create = False
        can_delete = False
    
    class AnswerOptionAdmin(ModelView, model=AnswerOption):
        column_list = [AnswerOption.id, AnswerOption.answer_id, AnswerOption.option_id]
        column_details_exclude_list = [AnswerOption.id, AnswerOption.answer_id, AnswerOption.option_id]
        can_create = True
        can_edit = True
        can_delete = True
        name = "Answer Option"
        name_plural = "Answer Options"
        icon = "fa-solid fa-check"
        
        # Make it read-only by default
        can_create = False
        can_delete = False
    
    # Notifications
    class NotificationAdmin(ModelView, model=Notification):
        column_list = [Notification.id, Notification.message, Notification.read, 
                      Notification.user_id, Notification.created_at]
        column_searchable_list = [Notification.message]
        column_sortable_list = [Notification.created_at, Notification.read]
        column_details_exclude_list = [Notification.id, Notification.user_id]
        can_create = True
        can_edit = True
        can_delete = True
        name = "Notification"
        name_plural = "Notifications"
        icon = "fa-solid fa-bell"
    
    # Admin Users Management
    class AdminUserAdmin(ModelView, model=AdminUser):
        column_list = [AdminUser.id, AdminUser.username, AdminUser.email, AdminUser.is_active, 
                      AdminUser.is_superuser, AdminUser.created_at, AdminUser.last_login]
        column_searchable_list = [AdminUser.username, AdminUser.email]
        column_sortable_list = [AdminUser.username, AdminUser.created_at, AdminUser.last_login]
        column_details_exclude_list = [AdminUser.id, AdminUser.password_hash]
        can_create = True
        can_edit = True
        can_delete = True
        name = "Admin User"
        name_plural = "Admin Users"
        icon = "fa-solid fa-user-shield"
        
        # Hide password hash from forms and display
        form_columns = [AdminUser.username, AdminUser.email, AdminUser.is_active, AdminUser.is_superuser]

    # Register all admin views
    admin.add_view(AdminUserAdmin)
    admin.add_view(UserAdmin)
    admin.add_view(UserProfileAdmin)
    admin.add_view(SurveyAdmin)
    admin.add_view(QuestionCategoryAdmin)
    admin.add_view(QuestionAdmin)
    admin.add_view(OptionAdmin)
    admin.add_view(AnswerAdmin)
    admin.add_view(AnswerOptionAdmin)
    admin.add_view(NotificationAdmin)
    
    return admin
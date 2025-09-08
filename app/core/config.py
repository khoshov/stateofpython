from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str = "postgresql://survey_user:survey_pass@localhost:5432/survey_db"
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Email settings
    mail_username: str = "khoshov@gmail.com"
    mail_password: str = "rzewdhgmvkdtkssk"
    mail_from: str = "hello@stateofpython.ru"
    mail_port: int = 587
    mail_server: str = "smtp.gmail.com"
    mail_from_name: str = "Survey API"
    mail_starttls: bool = True
    mail_ssl_tls: bool = False
    use_credentials: bool = True
    validate_certs: bool = True
    
    # Frontend URL for email links
    frontend_url: str = "http://localhost:3001"

    class Config:
        env_file = ".env"


settings = Settings()
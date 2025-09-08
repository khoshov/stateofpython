from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig
from app.core.config import settings
from typing import List
import logging

logger = logging.getLogger(__name__)

# Email configuration
conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_FROM_NAME=settings.mail_from_name,
    MAIL_STARTTLS=settings.mail_starttls,
    MAIL_SSL_TLS=settings.mail_ssl_tls,
    USE_CREDENTIALS=settings.use_credentials,
    VALIDATE_CERTS=settings.validate_certs
)

# Email templates
SURVEY_INVITATION_TEMPLATE = """
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 20px;">
    <div style="max-width: 600px; margin: 0 auto;">
        <div style="background: #007bff; color: white; padding: 20px; border-radius: 5px 5px 0 0;">
            <h1 style="margin: 0;">Survey API</h1>
            <p style="margin: 10px 0 0 0;">Приглашение на участие в опросе</p>
        </div>
        <div style="background: #f9f9f9; padding: 20px;">
            <h2>Здравствуйте!</h2>
            <p>Вы получили это письмо, потому что зарегистрировались для участия в опросе <strong>"{survey_title}"</strong>.</p>
            
            <p><strong>Описание опроса:</strong><br>
            {survey_description}</p>
            
            <p>Для начала прохождения опроса нажмите на кнопку ниже:</p>
            
            <a href="{survey_link}" style="display: inline-block; background: #007bff; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0;">Начать опрос</a>
            
            <p><small>Или скопируйте и вставьте эту ссылку в браузер:<br>
            {survey_link}</small></p>
            
            <p>Опрос займет примерно 5-10 минут. Ваши ответы помогут нам улучшить наши продукты и услуги.</p>
            
            <p>Спасибо за ваше время!</p>
        </div>
        <div style="background: #e9ecef; padding: 15px; border-radius: 0 0 5px 5px; font-size: 12px;">
            <p>Это письмо было отправлено автоматически. Пожалуйста, не отвечайте на него.</p>
            <p>Если у вас есть вопросы, свяжитесь с нами: support@example.com</p>
        </div>
    </div>
</body>
</html>
"""

class EmailService:
    def __init__(self):
        try:
            self.fastmail = FastMail(conf)
            self.enabled = True
        except Exception as e:
            logger.warning(f"Email service disabled due to configuration error: {e}")
            self.enabled = False
    
    async def send_survey_invitation(
        self,
        email: str,
        token: str,
        survey_title: str,
        survey_description: str = ""
    ) -> bool:
        """Send survey invitation email"""
        
        if not self.enabled:
            logger.info(f"Email service disabled. Would send survey invitation to {email} with token {token}")
            return True  # Return True for demo mode
        
        try:
            survey_link = f"{settings.frontend_url}/survey/{token}"
            
            html_content = SURVEY_INVITATION_TEMPLATE.format(
                survey_title=survey_title,
                survey_description=survey_description or "Примите участие в нашем исследовании",
                survey_link=survey_link
            )
            
            message = MessageSchema(
                subject=f"Приглашение на опрос: {survey_title}",
                recipients=[email],
                body=html_content,
                subtype=MessageType.html,
            )
            
            await self.fastmail.send_message(message)
            logger.info(f"Survey invitation sent successfully to {email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {email}: {e}")
            return False
    
    async def send_test_email(self, email: str) -> bool:
        """Send test email to verify configuration"""
        
        if not self.enabled:
            logger.info(f"Email service disabled. Would send test email to {email}")
            return True
        
        try:
            message = MessageSchema(
                subject="Test Email from Survey API",
                recipients=[email],
                body="<h1>Test Email</h1><p>If you receive this email, your email configuration is working correctly!</p>",
                subtype=MessageType.html,
            )
            
            await self.fastmail.send_message(message)
            logger.info(f"Test email sent successfully to {email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send test email to {email}: {e}")
            return False

# Global email service instance
email_service = EmailService()
#!/usr/bin/env python3
"""
Простой скрипт для быстрого создания администратора
Использование: python create_admin_simple.py username email password
"""

import sys
from app.core.database import SessionLocal
from app.models.models import AdminUser


def create_admin_simple(username: str, email: str, password: str, is_superuser: bool = True):
    """Создание администратора с параметрами"""
    
    db = SessionLocal()
    try:
        # Проверяем, не существует ли уже такой пользователь
        existing_user = db.query(AdminUser).filter(
            (AdminUser.username == username) | (AdminUser.email == email)
        ).first()
        
        if existing_user:
            print(f"❌ Пользователь с username '{username}' или email '{email}' уже существует!")
            return False
        
        # Создаем нового администратора
        admin_user = AdminUser.create_admin(
            username=username,
            email=email,
            password=password,
            is_superuser=is_superuser
        )
        
        db.add(admin_user)
        db.commit()
        
        print("✅ Администратор создан!")
        print(f"   👤 Username: {username}")
        print(f"   📧 Email: {email}")
        print(f"   🔑 Суперпользователь: {'Да' if is_superuser else 'Нет'}")
        print(f"   🆔 ID: {admin_user.id}")
        
        return True
        
    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка: {e}")
        return False
    finally:
        db.close()


def main():
    if len(sys.argv) < 4:
        print("Использование: python create_admin_simple.py <username> <email> <password> [superuser=true]")
        print("Пример: python create_admin_simple.py myuser user@example.com mypassword")
        sys.exit(1)
    
    username = sys.argv[1]
    email = sys.argv[2] 
    password = sys.argv[3]
    is_superuser = len(sys.argv) < 5 or sys.argv[4].lower() in ['true', '1', 'yes', 'да']
    
    success = create_admin_simple(username, email, password, is_superuser)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
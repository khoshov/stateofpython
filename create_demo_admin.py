#!/usr/bin/env python3
"""
Скрипт для автоматического создания демо администратора
"""

from app.core.database import SessionLocal
from app.models.models import AdminUser


def create_demo_admin():
    """Создание демо администратора"""
    
    print("🔧 Создание демо администратора...")
    
    db = SessionLocal()
    try:
        # Проверяем, не существует ли уже admin
        existing_admin = db.query(AdminUser).filter(AdminUser.username == "superadmin").first()
        
        if existing_admin:
            print("✅ Демо администратор 'superadmin' уже существует!")
            print(f"   📧 Email: {existing_admin.email}")
            print(f"   🔑 Суперпользователь: {'Да' if existing_admin.is_superuser else 'Нет'}")
            return True
        
        # Создаем нового администратора
        admin_user = AdminUser.create_admin(
            username="superadmin",
            email="admin@example.com",
            password="supersecret123",
            is_superuser=True
        )
        
        db.add(admin_user)
        db.commit()
        
        print("✅ Демо администратор создан!")
        print(f"   👤 Username: superadmin")
        print(f"   📧 Email: admin@example.com")
        print(f"   🔒 Password: supersecret123")
        print(f"   🔑 Суперпользователь: Да")
        print(f"   🆔 ID: {admin_user.id}")
        
        return True
        
    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка при создании администратора: {e}")
        return False
    finally:
        db.close()


if __name__ == "__main__":
    create_demo_admin()
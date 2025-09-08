#!/usr/bin/env python3
"""
Скрипт для создания суперпользователя админки
"""

import sys
import getpass
from app.core.database import SessionLocal
from app.models.models import AdminUser


def create_superuser():
    """Создание суперпользователя через командную строку"""
    
    print("🔧 Создание суперпользователя для админки Survey API")
    print("=" * 50)
    
    # Получаем данные от пользователя
    username = input("👤 Username: ").strip()
    if not username:
        print("❌ Username не может быть пустым!")
        return False
        
    email = input("📧 Email: ").strip()
    if not email:
        print("❌ Email не может быть пустым!")
        return False
    
    # Безопасный ввод пароля
    while True:
        password = getpass.getpass("🔒 Password: ")
        if len(password) < 4:
            print("❌ Пароль должен содержать минимум 4 символа!")
            continue
            
        password_confirm = getpass.getpass("🔒 Confirm password: ")
        if password != password_confirm:
            print("❌ Пароли не совпадают!")
            continue
        break
    
    # Проверяем, является ли это суперпользователем
    is_superuser_input = input("🔑 Является ли суперпользователем? (y/N): ").strip().lower()
    is_superuser = is_superuser_input in ['y', 'yes', 'да', 'д']
    
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
        
        print("\n✅ Суперпользователь успешно создан!")
        print(f"   👤 Username: {username}")
        print(f"   📧 Email: {email}")
        print(f"   🔑 Суперпользователь: {'Да' if is_superuser else 'Нет'}")
        print(f"   🆔 ID: {admin_user.id}")
        
        return True
        
    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка при создании пользователя: {e}")
        return False
    finally:
        db.close()


def list_admin_users():
    """Показать список всех админ пользователей"""
    
    print("👥 Список администраторов:")
    print("=" * 50)
    
    db = SessionLocal()
    try:
        admins = db.query(AdminUser).order_by(AdminUser.created_at).all()
        
        if not admins:
            print("Нет созданных администраторов")
            return
            
        for admin in admins:
            status = "🟢 Активен" if admin.is_active else "🔴 Неактивен"
            super_status = "🔑 Суперюзер" if admin.is_superuser else "👤 Обычный"
            print(f"• {admin.username} ({admin.email}) - {status} - {super_status}")
            print(f"  🆔 ID: {admin.id}")
            print(f"  📅 Создан: {admin.created_at}")
            if admin.last_login:
                print(f"  🕐 Последний вход: {admin.last_login}")
            print()
            
    except Exception as e:
        print(f"❌ Ошибка при получении списка: {e}")
    finally:
        db.close()


def main():
    """Главная функция"""
    
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        list_admin_users()
        return
    
    try:
        success = create_superuser()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Операция отменена пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
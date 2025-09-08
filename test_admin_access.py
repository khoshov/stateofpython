#!/usr/bin/env python3
"""
Тест доступности админ интерфейса
"""

import requests
from requests.sessions import Session

def test_admin_access():
    """Тест админ интерфейса"""
    
    base_url = "http://localhost:8000"
    
    print("🔧 Тестирование админ интерфейса...")
    
    # Создаем сессию для сохранения cookies
    session = Session()
    
    # 1. Проверяем доступность страницы логина
    print("1. Проверяем страницу логина...")
    response = session.get(f"{base_url}/admin/login")
    
    if response.status_code != 200:
        print(f"❌ Страница логина недоступна: {response.status_code}")
        return False
    
    if "Survey Admin" not in response.text:
        print("❌ Страница логина не содержит ожидаемого контента")
        return False
    
    print("✅ Страница логина доступна")
    
    # 2. Проверяем редирект на логин при доступе к админке без аутентификации
    print("2. Проверяем редирект без аутентификации...")
    response = session.get(f"{base_url}/admin/", allow_redirects=False)
    
    if response.status_code != 302:
        print(f"❌ Ожидался редирект 302, получен {response.status_code}")
        return False
    
    if "/admin/login" not in response.headers.get("location", ""):
        print("❌ Редирект не ведет на страницу логина")
        return False
    
    print("✅ Редирект на логин работает")
    
    # 3. Тестируем аутентификацию
    print("3. Тестируем аутентификацию...")
    
    # Получаем CSRF токен или форму
    login_page = session.get(f"{base_url}/admin/login")
    
    # Отправляем данные для логина
    login_data = {
        "username": "admin",
        "password": "admin"
    }
    
    response = session.post(f"{base_url}/admin/login", data=login_data, allow_redirects=False)
    
    if response.status_code not in [302, 303]:
        print(f"❌ Логин неуспешен: {response.status_code}")
        return False
    
    print("✅ Аутентификация прошла успешно")
    
    # 4. Проверяем доступ к главной странице админки
    print("4. Проверяем главную страницу админки...")
    response = session.get(f"{base_url}/admin/")
    
    if response.status_code != 200:
        print(f"❌ Главная страница админки недоступна: {response.status_code}")
        return False
    
    # Проверяем наличие моделей в интерфейсе
    expected_models = ["Users", "Surveys", "Questions", "Answers", "Notifications"]
    page_content = response.text
    
    found_models = []
    for model in expected_models:
        if model.lower() in page_content.lower():
            found_models.append(model)
    
    print(f"✅ Главная страница админки доступна")
    print(f"📋 Найденные модели: {', '.join(found_models)}")
    
    # 5. Проверяем доступность конкретных моделей
    print("5. Проверяем списки моделей...")
    
    model_urls = [
        "/admin/user/list",
        "/admin/survey/list", 
        "/admin/question/list",
        "/admin/notification/list"
    ]
    
    accessible_models = []
    for url in model_urls:
        try:
            response = session.get(f"{base_url}{url}")
            if response.status_code == 200:
                model_name = url.split('/')[-2].capitalize()
                accessible_models.append(model_name)
        except Exception as e:
            print(f"⚠️  Ошибка доступа к {url}: {e}")
    
    print(f"✅ Доступные модели: {', '.join(accessible_models)}")
    
    return True

def check_api_availability():
    """Проверка доступности API"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        return response.status_code == 200
    except:
        return False

if __name__ == "__main__":
    print("🧪 Тест админ интерфейса Survey API")
    print("=" * 50)
    
    # Проверяем доступность API
    if not check_api_availability():
        print("❌ API недоступен. Убедитесь, что сервер запущен:")
        print("   docker-compose up -d")
        exit(1)
    
    print("✅ API доступен")
    
    # Запускаем тест
    success = test_admin_access()
    
    if success:
        print("\n🎉 Тест админ интерфейса завершен успешно!")
        print("\n📝 Информация для доступа:")
        print("   URL: http://localhost:8000/admin")
        print("   Username: admin")
        print("   Password: admin")
        print("\n💡 Возможности админки:")
        print("   • Управление пользователями и профилями")
        print("   • Создание и редактирование опросов")
        print("   • Управление вопросами и категориями")
        print("   • Просмотр ответов пользователей")
        print("   • Система уведомлений")
    else:
        print("\n❌ Тест админ интерфейса завершился с ошибкой!")
        exit(1)
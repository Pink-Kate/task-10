#!/usr/bin/env python
"""
Швидкий запуск проекту Цитати
Автоматично налаштовує середовище та запускає сервер
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Виконує команду з виведенням опису"""
    print(f"\n==================================================")
    print(f"🚀 {description}")
    print(f"==================================================")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Помилка: {e}")
        print(f"Деталі: {e.stderr}")
        return False

def create_env_file():
    """Створює .env файл з базовими налаштуваннями"""
    env_content = """# Django налаштування
SECRET_KEY=django-insecure-your-secret-key-here-change-in-production
DEBUG=True

# База даних SQLite (використовується за замовчуванням)
# PostgreSQL налаштування (закоментовані для SQLite)
# DB_NAME=quotes_db
# DB_USER=postgres
# DB_PASSWORD=password
# DB_HOST=localhost
# DB_PORT=5432

# MongoDB налаштування
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB=quotes_db
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    print("✅ Файл .env створено")

def main():
    print("🎯 Ласкаво просимо до проекту Цитати!")
    print("Цей скрипт допоможе вам швидко налаштувати та запустити проект.\n")
    
    # Перевіряємо чи існує віртуальне середовище
    if not os.path.exists('venv'):
        print("📦 Створення віртуального середовища...")
        if not run_command("python -m venv venv", "Створення віртуального середовища"):
            return
    
    # Активація віртуального середовища
    if platform.system() == "Windows":
        activate_script = "venv\\Scripts\\activate"
        python_path = "venv\\Scripts\\python.exe"
        pip_path = "venv\\Scripts\\pip.exe"
    else:
        activate_script = "venv/bin/activate"
        python_path = "venv/bin/python"
        pip_path = "venv/bin/pip"
    
    # Створюємо .env файл якщо його немає
    if not os.path.exists('.env'):
        create_env_file()
    
    # Встановлюємо залежності
    if not run_command(f"{pip_path} install -r requirements.txt", "Встановлення залежностей"):
        return
    
    # Створюємо міграції
    if not run_command(f"{python_path} manage.py makemigrations", "Створення міграцій"):
        return
    
    # Застосовуємо міграції
    if not run_command(f"{python_path} manage.py migrate", "Застосування міграцій"):
        return
    
    # Ініціалізуємо початкові дані
    if not run_command(f"{python_path} manage.py init_data", "Ініціалізація початкових даних"):
        return
    
    print("\n🎉 Проект успішно налаштовано!")
    print("\n📋 Дані для входу:")
    print("   Логін: admin")
    print("   Пароль: admin123")
    
    # Питаємо чи запустити сервер
    response = input("\n🚀 Запустити сервер зараз? (y/n): ").lower().strip()
    if response in ['y', 'yes', 'так', 'да']:
        print("\n🌐 Запуск сервера...")
        print("📱 Сайт буде доступний за адресою: http://127.0.0.1:8000/")
        print("⏹️  Для зупинки сервера натисніть Ctrl+C")
        run_command(f"{python_path} manage.py runserver", "Запуск сервера")
    else:
        print("\n✅ Для запуску сервера виконайте команду:")
        print(f"   {python_path} manage.py runserver")

if __name__ == "__main__":
    main() 
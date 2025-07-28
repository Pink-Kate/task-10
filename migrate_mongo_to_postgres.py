#!/usr/bin/env python
"""
Скрипт для міграції даних з MongoDB до PostgreSQL
"""
import os
import sys
import django
from datetime import datetime
from pymongo import MongoClient
from django.utils import timezone

# Налаштування Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotes_project.settings')
django.setup()

from quotes.models import Author, Quote, Tag
from django.contrib.auth.models import User

def migrate_from_mongodb():
    """Міграція даних з MongoDB до PostgreSQL"""
    
    # Підключення до MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['quotes_db']
    
    # Створення користувача за замовчуванням
    default_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        default_user.set_password('admin123')
        default_user.save()
        print(f"Створено користувача за замовчуванням: {default_user.username}")
    
    # Міграція авторів
    print("Мігруємо авторів...")
    authors_collection = db['authors']
    for mongo_author in authors_collection.find():
        author, created = Author.objects.get_or_create(
            name=mongo_author.get('name', 'Невідомий автор'),
            defaults={
                'bio': mongo_author.get('bio', ''),
                'birth_date': mongo_author.get('birth_date'),
                'death_date': mongo_author.get('death_date'),
                'created_by': default_user,
            }
        )
        if created:
            print(f"Додано автора: {author.name}")
    
    # Міграція тегів
    print("Мігруємо теги...")
    tags_collection = db['tags']
    for mongo_tag in tags_collection.find():
        tag, created = Tag.objects.get_or_create(
            name=mongo_tag.get('name', 'untagged')
        )
        if created:
            print(f"Додано тег: {tag.name}")
    
    # Міграція цитат
    print("Мігруємо цитати...")
    quotes_collection = db['quotes']
    for mongo_quote in quotes_collection.find():
        # Знаходимо автора
        author_name = mongo_quote.get('author', 'Невідомий автор')
        author, _ = Author.objects.get_or_create(
            name=author_name,
            defaults={
                'bio': '',
                'created_by': default_user,
            }
        )
        
        # Створюємо цитату
        quote, created = Quote.objects.get_or_create(
            text=mongo_quote.get('text', ''),
            author=author,
            defaults={
                'created_by': default_user,
            }
        )
        
        if created:
            # Додаємо теги
            mongo_tags = mongo_quote.get('tags', [])
            for tag_name in mongo_tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                quote.tags.add(tag)
            
            print(f"Додано цитату: {quote.text[:50]}...")
    
    print("Міграція завершена!")
    print(f"Авторів: {Author.objects.count()}")
    print(f"Цитат: {Quote.objects.count()}")
    print(f"Тегів: {Tag.objects.count()}")

if __name__ == '__main__':
    migrate_from_mongodb() 
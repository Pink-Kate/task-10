from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from quotes.models import Author, Quote, Tag
from datetime import date

class Command(BaseCommand):
    help = 'Ініціалізація початкових даних для сайту цитат'

    def handle(self, *args, **options):
        # Створення суперкористувача
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(
                self.style.SUCCESS('Створено суперкористувача: admin/admin123')
            )

        # Створення авторів
        authors_data = [
            {
                'name': 'Альберт Ейнштейн',
                'bio': 'Німецький фізик-теоретик, один з засновників сучасної теоретичної фізики.',
                'birth_date': date(1879, 3, 14),
                'death_date': date(1955, 4, 18)
            },
            {
                'name': 'Марк Твен',
                'bio': 'Американський письменник, журналіст і громадський діяч.',
                'birth_date': date(1835, 11, 30),
                'death_date': date(1910, 4, 21)
            },
            {
                'name': 'Оскар Вайлд',
                'bio': 'Ірландський письменник, поет, драматург.',
                'birth_date': date(1854, 10, 16),
                'death_date': date(1900, 11, 30)
            },
            {
                'name': 'Фрідріх Ніцше',
                'bio': 'Німецький філософ, культуролог, композитор.',
                'birth_date': date(1844, 10, 15),
                'death_date': date(1900, 8, 25)
            },
            {
                'name': 'Лев Толстой',
                'bio': 'Російський письменник і мислитель.',
                'birth_date': date(1828, 9, 9),
                'death_date': date(1910, 11, 20)
            }
        ]

        for author_data in authors_data:
            author, created = Author.objects.get_or_create(
                name=author_data['name'],
                defaults={
                    'bio': author_data['bio'],
                    'birth_date': author_data['birth_date'],
                    'death_date': author_data['death_date'],
                    'created_by': admin_user
                }
            )
            if created:
                self.stdout.write(f'Додано автора: {author.name}')

        # Створення тегів
        tags_data = ['мудрість', 'життя', 'любов', 'філософія', 'наука', 'мистецтво', 'освіта', 'успіх']
        
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if created:
                self.stdout.write(f'Додано тег: {tag.name}')

        # Створення цитат
        quotes_data = [
            {
                'text': 'Життя - це те, що з тобою відбувається, поки ти зайнятий іншими планами.',
                'author_name': 'Джон Леннон',
                'tags': ['життя', 'мудрість']
            },
            {
                'text': 'Єдиний спосіб робити великі справи - любити те, що ти робиш.',
                'author_name': 'Стів Джобс',
                'tags': ['успіх', 'життя']
            },
            {
                'text': 'Будь зміною, якою хочеш бачити світ.',
                'author_name': 'Махатма Ганді',
                'tags': ['мудрість', 'життя']
            },
            {
                'text': 'Успіх - це вміння переходити від однієї невдачі до іншої, не втрачаючи ентузіазму.',
                'author_name': 'Вінстон Черчилль',
                'tags': ['успіх', 'мудрість']
            },
            {
                'text': 'Найкращий час посадити дерево було 20 років тому. Другий найкращий час - зараз.',
                'author_name': 'Китайська прислів\'я',
                'tags': ['мудрість', 'життя']
            },
            {
                'text': 'Освіта - це не підготовка до життя; освіта - це і є життя.',
                'author_name': 'Джон Дьюї',
                'tags': ['освіта', 'життя']
            },
            {
                'text': 'Мистецтво - це брехня, яка дозволяє нам зрозуміти правду.',
                'author_name': 'Пабло Пікассо',
                'tags': ['мистецтво', 'філософія']
            },
            {
                'text': 'Наука без релігії кульгава, релігія без науки сліпа.',
                'author_name': 'Альберт Ейнштейн',
                'tags': ['наука', 'філософія']
            }
        ]

        for quote_data in quotes_data:
            # Створюємо автора, якщо його немає
            author, _ = Author.objects.get_or_create(
                name=quote_data['author_name'],
                defaults={
                    'bio': '',
                    'created_by': admin_user
                }
            )
            
            # Створюємо цитату
            quote, created = Quote.objects.get_or_create(
                text=quote_data['text'],
                author=author,
                defaults={
                    'created_by': admin_user
                }
            )
            
            if created:
                # Додаємо теги
                for tag_name in quote_data['tags']:
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    quote.tags.add(tag)
                
                self.stdout.write(f'Додано цитату: {quote.text[:50]}...')

        self.stdout.write(
            self.style.SUCCESS('Ініціалізація даних завершена успішно!')
        ) 
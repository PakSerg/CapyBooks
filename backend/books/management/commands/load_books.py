from django.core.management.base import BaseCommand
from books.models import Book, Author, Genre
from faker import Faker
import random

fake = Faker('ru_RU')

class Command(BaseCommand):
    help = 'Загружает тестовые данные книг, авторов и жанров'

    def handle(self, *args, **kwargs):
        genres = [
            'Фэнтези', 'Научная фантастика', 'Детектив', 'Роман', 'Поэзия',
            'Исторический роман', 'Приключения', 'Ужасы', 'Классика', 'Биография'
        ]
        
        genre_objects = []
        for genre_name in genres:
            genre, created = Genre.objects.get_or_create(name=genre_name)
            genre_objects.append(genre)
            if created:
                self.stdout.write(f'Создан жанр: {genre_name}')

        famous_books = [
            {'name': 'Война и мир', 'author': 'Лев Толстой', 'year': 1869},
            {'name': 'Преступление и наказание', 'author': 'Фёдор Достоевский', 'year': 1866},
            {'name': 'Мастер и Маргарита', 'author': 'Михаил Булгаков', 'year': 1967},
            {'name': 'Евгений Онегин', 'author': 'Александр Пушкин', 'year': 1833},
            {'name': 'Идиот', 'author': 'Фёдор Достоевский', 'year': 1869},
            {'name': 'Анна Каренина', 'author': 'Лев Толстой', 'year': 1877},
            {'name': 'Герой нашего времени', 'author': 'Михаил Лермонтов', 'year': 1840},
            {'name': 'Мёртвые души', 'author': 'Николай Гоголь', 'year': 1842},
            {'name': 'Тихий Дон', 'author': 'Михаил Шолохов', 'year': 1940},
            {'name': 'Братья Карамазовы', 'author': 'Фёдор Достоевский', 'year': 1880},
            {'name': 'Гарри Поттер и философский камень', 'author': 'Джоан Роулинг', 'year': 1997},
            {'name': 'Властелин колец', 'author': 'Джон Толкин', 'year': 1954},
            {'name': '1984', 'author': 'Джордж Оруэлл', 'year': 1949},
            {'name': 'Убить пересмешника', 'author': 'Харпер Ли', 'year': 1960},
            {'name': 'Великий Гэтсби', 'author': 'Фрэнсис Скотт Фицджеральд', 'year': 1925},
            {'name': 'Гордость и предубеждение', 'author': 'Джейн Остин', 'year': 1813},
            {'name': 'Три товарища', 'author': 'Эрих Мария Ремарк', 'year': 1936},
            {'name': 'Сто лет одиночества', 'author': 'Габриэль Гарсиа Маркес', 'year': 1967},
            {'name': 'Алхимик', 'author': 'Пауло Коэльо', 'year': 1988},
            {'name': 'Маленький принц', 'author': 'Антуан де Сент-Экзюпери', 'year': 1943},
        ]

        for book_data in famous_books:
            author_name = book_data['author'].split()
            author = Author.objects.create(
                last_name=author_name[-1],
                first_name=author_name[0],
                middle_name=author_name[1] if len(author_name) > 2 else None
            )

            book = Book.objects.create(
                name=book_data['name'],
                author=author,
                year=book_data['year'],
                pages_count=random.randint(200, 800),
                description=fake.text(max_nb_chars=500)
            )

            book.genres.add(*random.sample(genre_objects, k=random.randint(1, 3)))
            
            self.stdout.write(f'Создана книга: {book.name}')

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно загружены!')) 
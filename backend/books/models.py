from django.db import models
import uuid
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from transliterate import translit


class Author(models.Model): 
    last_name = models.CharField('Фамилия', null=True, blank=True, max_length=150) 
    first_name = models.CharField('Имя', max_length=150)
    middle_name = models.CharField('Второе имя', max_length=150, null=True, blank=True)
    patronymic = models.CharField('Отчество', max_length=150, null=True, blank=True)
    slug = models.SlugField('Слаг', max_length=150, null=True, blank=True)

    class Meta: 
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы' 

    def __str__(self) -> str: 
        return f'{self.last_name if self.last_name else ""} {self.middle_name if self.middle_name else ""} {self.first_name if self.first_name else ""} {self.patronymic if self.patronymic else ""}'.strip()

    def save(self, *args, **kwargs):
        if not self.slug:
            name_parts = [
                self.last_name,
                self.first_name,
                self.middle_name,
                self.patronymic
            ]
            self.slug = '-'.join(
                slugify(translit(str(part), 'ru', reversed=True))
                for part in name_parts if part
            )
        
        super(Author, self).save(*args, **kwargs)


class Genre(models.Model): 
    name = models.CharField('Название', unique=True) 

    class Meta: 
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'  

    def __str__(self) -> str: 
        return f'{self.name}'


class Book(models.Model):
    name = models.CharField('Название', max_length=500) 
    author = models.ForeignKey(
        verbose_name='Автор', to=Author, on_delete=models.SET_DEFAULT, default=None, null=True, 
        blank=True, related_name='author_books'
    ) 
    image = models.ImageField('Фото', upload_to='books/', null=True, blank=True) 
    pages_count = models.SmallIntegerField('Кол-во страниц', null=True, blank=True, validators=[MinValueValidator(1)])
    year = models.SmallIntegerField('Год', null=True, blank=True)
    description = models.TextField('Описание', max_length=2000, null=True, blank=True) 
    genres = models.ManyToManyField(verbose_name='Жанры', to=Genre, related_name='genre_books') 
    slug = models.SlugField('Слаг', max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs): 
        if not self.slug: 
            self.slug = slugify(translit(str(self.name), language_code='ru', reversed=True))

        return super(Book, self).save(*args, **kwargs)

    class Meta: 
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'  

    def __str__(self) -> str: 
        return f'{self.name}'


class BookPhoto(models.Model): 
    image = models.ImageField(verbose_name='Фото',upload_to='books/additional/') 
    book = models.ForeignKey(verbose_name='Книга', to=Book, on_delete=models.CASCADE, related_name='photos')

    class Meta: 
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'  

    def __str__(self) -> str: 
        return f'{self.book.name} {self.pk}'
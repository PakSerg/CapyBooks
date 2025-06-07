from django.db import models
import uuid
from django.core.validators import MinValueValidator


class Author(models.Model): 
    last_name = models.CharField('Фамилия', null=True, blank=True, max_length=150) 
    first_name = models.CharField('Имя', max_length=150)
    middle_name = models.CharField('Второе имя', max_length=150, null=True, blank=True)
    patronymic = models.CharField('Отчество', max_length=150, null=True, blank=True)

    class Meta: 
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы' 

    def __str__(self) -> str: 
        return f'{self.last_name} {self.first_name} {self.patronymic}'
    

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

    class Meta: 
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'  

    def __str__(self) -> str: 
        return f'{self.name}'

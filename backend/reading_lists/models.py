from django.db import models
from django.contrib.auth.models import User
from books.models import Book


class UserBookStatus(models.Model): 
    name = models.CharField('Название', max_length=100)

    class Meta: 
        verbose_name = 'Статус' 
        verbose_name_plural = 'Статусы'

    def __str__(self) -> str:
        return f'{self.name}'
    
    @staticmethod
    def get_open() -> 'UserBookStatus': 
        return UserBookStatus.objects.get_or_create(name='OPEN')[0]
    
    @staticmethod
    def get_progress() -> 'UserBookStatus': 
        return UserBookStatus.objects.get_or_create(name='PROGRESS')[0]
    
    @staticmethod
    def get_done() -> 'UserBookStatus': 
        return UserBookStatus.objects.get_or_create(name='DONE')[0]


class UserBook(models.Model): 
    user = models.ForeignKey(verbose_name='Пользователь', to=User, on_delete=models.CASCADE, related_name='user_reading') 
    book = models.ForeignKey(verbose_name='Книга', to=Book, on_delete=models.CASCADE, related_name='book_reading')
    status = models.ForeignKey(verbose_name='Статус', to=UserBookStatus, on_delete=models.SET_NULL, null=True, blank=True) 
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True) 
    started_at = models.DateField('Дата начала чтения', null=True, blank=True)
    finished_at = models.DateField('Дата окончания чтения', null=True, blank=True)
    notes = models.TextField('Заметки', max_length=2000, null=True, blank=True) 

    class Meta: 
        verbose_name = 'Элемент списка' 
        verbose_name_plural = 'Списки'

    def __str__(self) -> str:
        return f'{self.book.name} | {self.user.username} | {self.status}'
    
    def save(self, *args, **kwargs): 
        if not self.status: 
            self.status = UserBookStatus.get_open() 
        return super(UserBook, self).save(*args, **kwargs)
from django.contrib import admin
from .models import (
    Book, 
    Author, 
    Genre, 
    BookPhoto,
)


admin.site.register(Genre)


@admin.register(Author) 
class AuthorAdmin(admin.ModelAdmin): 
    list_display = ('last_name', 'first_name', 'patronymic', 'slug')


class BookPhotoInline(admin.TabularInline): 
    model = BookPhoto


@admin.register(Book) 
class BookAdmin(admin.ModelAdmin): 
    list_display = ('name', 'author')
    prepopulated_fields = {'slug': ('name',)}
    inlines = (BookPhotoInline,)

from django.contrib import admin
from .models import Book, Author, Genre


admin.site.register(Genre)


@admin.register(Author) 
class AuthorAdmin(admin.ModelAdmin): 
    list_display = ('last_name', 'first_name', 'patronymic', 'slug')
    # readonly_fields = ('slug',)


@admin.register(Book) 
class BookAdmin(admin.ModelAdmin): 
    list_display = ('name', 'author')
    prepopulated_fields = {'slug': ('name',)}
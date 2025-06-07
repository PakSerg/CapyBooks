from django.contrib import admin
from .models import (
    Book, 
    Author, 
    Genre,
)


admin.register(Book) 

admin.register(Author) 

admin.register(Genre)
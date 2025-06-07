from django.contrib import admin
from .models import UserBook, UserBookStatus


@admin.register(UserBook) 
class UserBookAdmin(admin.ModelAdmin): 
    list_display = ('__str__',) 


@admin.register(UserBookStatus)
class UserBookStatusAdmin(admin.ModelAdmin): 
    list_display = ('name',)
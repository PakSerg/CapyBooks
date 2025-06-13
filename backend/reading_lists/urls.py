from django.urls import path
from .views import *


app_name = 'reading_lists'


urlpatterns = [
    path('', ReadingListView.as_view()),
    path('statistics/', StatisticsView.as_view()),
    path('statuses/', StatusesView.as_view()),
    path('add-book/', AddBookView.as_view()), 
    path('update-book/', UpdateBookView.as_view()), 
    path('delete-book/', DeleteBookView.as_view()),
]
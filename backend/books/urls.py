from django.urls import path
from .views import *


app_name = 'books'


urlpatterns = [
    path('', CatalogView.as_view(), name='catalog'), 
    path('popular/', PopularBooksView.as_view(), name='popular'),
    path('genres/', GenresView.as_view()),
    path('<str:slug>/', BookView.as_view(), name='book'),
]
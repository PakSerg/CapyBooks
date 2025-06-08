from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .models import Book, Genre
from django.shortcuts import get_object_or_404
from .serializers import serialize_book, serialize_genre
from reading_lists.models import UserBook


class CatalogView(APIView):
    def get(self, request): 
        books = Book.objects.select_related('author').prefetch_related('genres').all()
        user_books = []
        if request.user.is_authenticated:
            user_books = UserBook.objects.filter(user=request.user).values_list('book_id', flat=True)
        result = {
            'books': [
                serialize_book(book) for book in books
            ], 
            'user_books': list(user_books)
        }
        return JsonResponse(result)
    

class BookView(APIView):
    def get(self, request, slug: str): 
        book = get_object_or_404(
            Book.objects.select_related('author').prefetch_related('genres'),
            slug=slug
        )
        result = {
            'book': serialize_book(book)
        }
        return JsonResponse(result)
    

class GenresView(APIView):
    def get(self, request): 
        genres = Genre.objects.all() 
        result = {
            'genres': [
                serialize_genre(genre) for genre in genres
            ]
        }
        return JsonResponse(result)
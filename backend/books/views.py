from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .models import Book, Genre
from django.shortcuts import get_object_or_404
from .serializers import serialize_book, serialize_genre
from reading_lists.models import UserBook
from django.db.models import Count, Q



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
        is_in_user_list = UserBook.objects.filter(
            user=request.user, 
            book=book
        ).first()

        user_books = []
        if request.user.is_authenticated:
            user_books = UserBook.objects.filter(user=request.user).values_list('book_id', flat=True)

        genre_ids = book.genres.values_list('id', flat=True)

        recommended_books = (
            Book.objects
            .exclude(id=book.id)
            .filter(genres__in=genre_ids)
            .annotate(same_genres=Count('genres', filter=Q(genres__in=genre_ids)))
            .order_by('-same_genres')
            .prefetch_related('genres', 'author')[:6]
        )

        result = {
            'book': serialize_book(book), 
            'is_in_user_list': bool(is_in_user_list),
            'recommended': [
                serialize_book(book) for book in recommended_books
            ],
            'user_books': list(user_books),
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
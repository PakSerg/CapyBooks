from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .models import Book, Genre
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from .serializers import serialize_book, serialize_genre
from reading_lists.models import UserBook
from django.db.models import Count, Q



class CatalogView(APIView):
    def get(self, request): 
        category_id = request.GET.get('category')  
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 15))  

        books_qs = Book.objects.select_related('author').prefetch_related('genres').all()

        if category_id:
            books_qs = books_qs.filter(genres__id=category_id)

        paginator = Paginator(books_qs, page_size)
        try:
            books_page = paginator.page(page)
        except EmptyPage:
            books_page = []

        user_books = []
        if request.user.is_authenticated:
            user_books = UserBook.objects.filter(user=request.user).values_list('book_id', flat=True)

        result = {
            'books': [
                serialize_book(book) for book in books_page
            ],
            'user_books': list(user_books),
            'pagination': {
                'current_page': page,
                'page_size': page_size,
                'total_pages': paginator.num_pages,
                'total_items': paginator.count,
            }
        }
        return JsonResponse(result)
    

class PopularBooksView(APIView): 
    def get(self, request): 
        popular_books = Book.objects.order_by('?')[:8]
        result = {
            'popular_books': [
                serialize_book(book) for book in popular_books
            ]
        }
        return JsonResponse(result)

    

class BookView(APIView):
    def get(self, request, slug: str): 
        book = get_object_or_404(
            Book.objects.select_related('author').prefetch_related('genres'),
            slug=slug
        )
        is_in_user_list = False
        if request.user.is_authenticated:
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
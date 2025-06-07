from django.shortcuts import render
from django.views import View 
from django.http import JsonResponse
from .models import Book
from django.shortcuts import get_object_or_404
from .serializers import serialize_book


class CatalogView(View): 
    def get(self, request): 
        books = Book.objects.select_related('author').prefetch_related('genres').all()
        result = {
            'books': [serialize_book(book) for book in books]
        }
        return JsonResponse(result)
    

class BookView(View): 
    def get(self, request, slug: str): 
        book = get_object_or_404(
            Book.objects.select_related('author').prefetch_related('genres'),
            slug=slug
        )
        result = {
            'book': serialize_book(book)
        }
        return JsonResponse(result)
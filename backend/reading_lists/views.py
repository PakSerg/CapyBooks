from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
import json
from books.models import Book
from django.contrib.auth.models import User
from .models import UserBook, UserBookStatus
from .exceptions import BookIsAlreadyAddedError
from datetime import datetime
from books.serializers import serialize_book


class ReadingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request): 
        user_books = UserBook.objects.select_related('book', 'status').filter(user=request.user)
        result = {
            'books': [
                serialize_book(user_book.book) for user_book in user_books
            ]
        }
        return JsonResponse(result)


class AddBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request): 
        try:
            data = json.loads(request.body)
            book_id = data.get('book_id')
            book = Book.objects.get(pk=book_id)
            
            user = request.user 

            user_book, created = UserBook.objects.get_or_create(
                user=user, 
                book=book
            )

            if not created: 
                raise BookIsAlreadyAddedError

            return JsonResponse({'message': 'Книга успешно добавлена в список'})

        except Book.DoesNotExist as e: 
            return JsonResponse({'error': f'Книга с id = {book_id} не найдена'})
        except BookIsAlreadyAddedError as e: 
            return JsonResponse({'error': 'Книга уже добавлена в список'})
        except Exception as e: 
            return JsonResponse({'error': str(e)})


class UpdateBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = json.loads(request.body)
            book_id = data.get('book_id')
            
            if not book_id:
                return JsonResponse({'error': 'Не указан id книги'})

            user_book = UserBook.objects.select_related('book', 'status').get(
                user=request.user,
                book_id=book_id
            )

            if 'status_id' in data:
                try:
                    status = UserBookStatus.objects.get(pk=data['status_id'])
                    user_book.status = status
                except UserBookStatus.DoesNotExist:
                    return JsonResponse({'error': 'Указанный статус не существует'})

            if 'notes' in data:
                user_book.notes = data['notes']

            if 'start_date' in data:
                try:
                    user_book.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
                except ValueError:
                    return JsonResponse({'error': 'Неверный формат даты начала чтения'})

            if 'end_date' in data:
                try:
                    user_book.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
                except ValueError:
                    return JsonResponse({'error': 'Неверный формат даты окончания чтения'})

            if 'rating' in data:
                rating = data['rating']
                if isinstance(rating, (int, float)) and 0 <= rating <= 10:
                    user_book.rating = rating
                else:
                    return JsonResponse({'error': 'Рейтинг должен быть числом от 0 до 10'})

            user_book.save()
            return JsonResponse({
                'message': 'Данные книги успешно обновлены',
                'book': {
                    'id': user_book.id,
                    'book_id': user_book.book.id,
                    'status_id': user_book.status.id if user_book.status else None,
                    'notes': user_book.notes,
                    'start_date': user_book.start_date.isoformat() if user_book.start_date else None,
                    'end_date': user_book.end_date.isoformat() if user_book.end_date else None,
                    'rating': user_book.rating
                }
            })

        except UserBook.DoesNotExist:
            return JsonResponse({'error': 'Книга не найдена в списке чтения'})
        except Exception as e:
            return JsonResponse({'error': str(e)})


class DeleteBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = json.loads(request.body)
            book_id = data.get('book_id')

            user_book = UserBook.objects.select_related('book').get(
                user=request.user,
                book_id=book_id
            )
            user_book.delete()

            return JsonResponse({'message': 'Книга успешно удалена из списка'})

        except UserBook.DoesNotExist:
            return JsonResponse({'error': 'Книга не найдена в списке чтения'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
        


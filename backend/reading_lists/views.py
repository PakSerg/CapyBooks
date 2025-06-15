from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
import json
from django.db.models.functions import TruncMonth
from collections import Counter
from django.db.models import Count
from books.models import Book
from django.contrib.auth.models import User
from .models import UserBook, UserBookStatus
from .exceptions import BookIsAlreadyAddedError
from datetime import datetime
from .serializers import serialize_user_book
from books.serializers import serialize_book
from datetime import datetime, timedelta
from django.utils.timezone import now
from .models import UserBookStatus


class ReadingListView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        user_books = UserBook.objects.select_related('book', 'status').filter(user=request.user)

        print(request.user)

        print(user_books)

        now_date = now().date()
        one_week_ago = now_date - timedelta(days=7)
        one_month_ago = now_date - timedelta(days=30)
        one_year_ago = now_date - timedelta(days=365)

        last_week_books = []
        last_month_books = []
        last_year_books = []
        all_time_books = []

        for ub in user_books:
            updated = ub.updated_at.date()
            if updated >= one_week_ago:
                last_week_books.append(ub)
            elif one_week_ago > updated >= one_month_ago:
                last_month_books.append(ub)
            elif one_month_ago > updated >= one_year_ago:
                last_year_books.append(ub)
            else:
                all_time_books.append(ub)

        result = {
            'all_books': [serialize_user_book(ub) for ub in user_books],
            'last_week': [serialize_user_book(ub) for ub in last_week_books],
            'last_month': [serialize_user_book(ub) for ub in last_month_books],
            'last_year': [serialize_user_book(ub) for ub in last_year_books],
            'older': [serialize_user_book(ub) for ub in all_time_books],
        }

        print(result)

        return JsonResponse(result)
    

class StatusesView(APIView): 
    def get(self, request): 
        statuses = UserBookStatus.objects.all()
        result = {
            'statuses': [
                {
                    'id': status.id, 
                    'name': status.name 
                }
                for status in statuses
            ]
        }
        return JsonResponse(result)


class AddBookView(APIView):
    # permission_classes = [IsAuthenticated]

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
    # permission_classes = [IsAuthenticated]

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

            print(data)

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
    # permission_classes = [IsAuthenticated]

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
        

class StatisticsView(APIView): 
    def get(self, request): 
        user = request.user
        user_books = UserBook.objects.filter(user=request.user, status=UserBookStatus.get_done()).select_related('book__author').prefetch_related('book__genres')

        print(user_books)

        authors = [ub.book.author for ub in user_books if ub.book.author is not None]
        top_authors = Counter(authors).most_common(3)
        top_authors_data = [{'author_id': author.id, 'author_name': str(author), 'books_count': count} for author, count in top_authors]

        genres = []
        for ub in user_books:
            genres.extend(list(ub.book.genres.all()))
        top_genres = Counter(genres).most_common(3)
        top_genres_data = [{'genre_id': genre.id, 'genre_name': genre.name, 'books_count': count} for genre, count in top_genres]

        result = {
            'top_authors': top_authors_data,
            'top_genres': top_genres_data,
        }
        print(result)

        return JsonResponse(result)


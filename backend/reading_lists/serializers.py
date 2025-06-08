from .models import UserBook
from books.serializers import MEDIA_DOMAIN


def serialize_user_book(user_book: UserBook) -> dict: 
    book = user_book.book
    return {
        'id': book.id,
        'name': book.name,
        'author': {
            'id': book.author.id,
            'name': str(book.author)
        } if book.author else None,
        'image': f'{MEDIA_DOMAIN}{book.image.url}' if book.image else None,
        'pages_count': book.pages_count,
        'year': book.year,
        'status': {
            'id': user_book.status.id, 
            'name': user_book.status.name,
        },
        'description': book.description,
        'genres': [
            {
                'id': genre.id, 
                'name': genre.name
            } for genre in book.genres.all()
        ],
        'slug': book.slug
    }
from .models import Book, Genre


def serialize_book(book: Book) -> dict:
    return {
        'id': book.id,
        'name': book.name,
        'author': {
            'id': book.author.id,
            'name': str(book.author)
        } if book.author else None,
        'image': book.image.url if book.image else None,
        'pages_count': book.pages_count,
        'year': book.year,
        'description': book.description,
        'genres': [
            {
                'id': genre.id, 
                'name': genre.name
            } for genre in book.genres.all()
        ],
        'slug': book.slug
    }


def serialize_genre(genre: Genre) -> dict: 
    return {
        'id': genre.id, 
        'name': genre.name
    }
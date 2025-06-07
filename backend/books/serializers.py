from django.db.models import QuerySet


def serialize_book(book: QuerySet) -> dict:
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
        'genres': [{'id': genre.id, 'name': genre.name} for genre in book.genres.all()],
        'slug': book.slug
    }
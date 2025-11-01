from typing import Optional
from models import Book, User, Library
from exceptions import BookNotAvailable, BookNotFound
from decorators import log_operation


@log_operation
def add_book(library: Library, book: Book) -> Library:
    library.books.append(book)
    return library


@log_operation
def find_book(library: Library, title: str) -> Optional[Book]:
    for book in library.books:
        if book.title.lower() == title.lower():
            return book
    return None


@log_operation
def is_book_borrow(library: Library, title: str, user: User) -> bool:
    book = find_book(library, title)

    if not book:
        raise BookNotFound(f"Книга '{title}' не найдена")

    if not book.available:
        raise BookNotAvailable(f"Книга '{title}' уже выдана")

    book.available = False
    return True


@log_operation
def return_book(library: Library, title: str, user: User) -> bool:
    book = find_book(library, title)

    if not book:
        raise BookNotFound(f"Книга '{title}' не найдена")

    book.available = True
    return True
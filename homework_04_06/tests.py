from models import Book, User, Library
from library import add_book, find_book, is_book_borrow, return_book
from exceptions import BookNotAvailable, BookNotFound
import pytest


def test_create_book():
    book = Book(title="Тест", author="Автор", year=2020, categories=["роман"])
    assert book.title == "Тест"
    assert book.available == True


def test_book_categories_normalized():
    book = Book(title="Тест", author="Автор", year=2020,
                categories=["Роман", "РОМАН", "классика"])
    assert len(book.categories) == 2
    assert "роман" in book.categories


def test_invalid_year():
    with pytest.raises(Exception):
        Book(title="Тест", author="Автор", year=3000, categories=[])


def test_invalid_email():
    with pytest.raises(Exception):
        User(name="Тест", email="invalid", membership_id="U001")


def test_add_book():
    library = Library()
    book = Book(title="Тест", author="Автор", year=2020, categories=[])
    add_book(library, book)
    assert library.total_books() == 1


def test_find_book():
    library = Library()
    book = Book(title="Война и мир", author="Толстой", year=1869, categories=[])
    add_book(library, book)
    found = find_book(library, "война и мир")
    assert found is not None


def test_borrow_book():
    library = Library()
    book = Book(title="Тест", author="Автор", year=2020, categories=[])
    user = User(name="Иван", email="ivan@mail.com", membership_id="U001")
    add_book(library, book)

    is_book_borrow(library, "Тест", user)
    assert library.available_books() == 0


def test_borrow_unavailable_book():
    library = Library()
    book = Book(title="Тест", author="Автор", year=2020, categories=[])
    user1 = User(name="Иван", email="ivan@mail.com", membership_id="U001")
    user2 = User(name="Петр", email="petr@mail.com", membership_id="U002")

    add_book(library, book)
    is_book_borrow(library, "Тест", user1)

    with pytest.raises(BookNotAvailable):
        is_book_borrow(library, "Тест", user2)


def test_return_book():
    library = Library()
    book = Book(title="Тест", author="Автор", year=2020, categories=[])
    user = User(name="Иван", email="ivan@mail.com", membership_id="U001")

    add_book(library, book)
    is_book_borrow(library, "Тест", user)
    return_book(library, "Тест", user)

    assert library.available_books() == 1
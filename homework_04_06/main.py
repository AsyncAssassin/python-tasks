from models import Book, User, Library
from library import add_book, find_book, is_book_borrow, return_book
from exceptions import BookNotAvailable, BookNotFound


def main():
    # Создаем библиотеку
    library = Library()

    # Добавляем книги
    book1 = Book(
        title="Война и мир",
        author="Лев Толстой",
        year=1869,
        categories=["классика", "роман"]
    )

    book2 = Book(
        title="1984",
        author="Джордж Оруэлл",
        year=1949,
        categories=["антиутопия"]
    )

    library = add_book(library, book1)
    library = add_book(library, book2)

    print(f"\nВсего книг: {library.total_books()}")
    print(f"Доступно: {library.available_books()}\n")

    # Создаем пользователя
    user = User(
        name="Тестов Иван",
        email="ivantest@example.com",
        membership_id="USER001"
    )

    # Выдаем книгу
    try:
        is_book_borrow(library, "Война и мир", user)
        print(f"Книга выдана. Доступно: {library.available_books()}\n")
    except (BookNotAvailable, BookNotFound) as e:
        print(f"Ошибка: {e}\n")

    # Пытаемся взять ту же книгу
    try:
        is_book_borrow(library, "Война и мир", user)
    except BookNotAvailable as e:
        print(f"Ожидаемая ошибка: {e}\n")

    # Возвращаем книгу
    return_book(library, "Война и мир", user)
    print(f"Книга возвращена. Доступно: {library.available_books()}\n")

    # Проверяем валидацию
    print("Тест валидации:")
    try:
        invalid_book = Book(
            title="Книга",
            author="Автор",
            year=3000,
            categories=[]
        )
    except Exception as e:
        print(f"Валидация года работает: {type(e).__name__}")

    try:
        invalid_user = User(
            name="Тест",
            email="invalid-email",
            membership_id="USER002"
        )
    except Exception as e:
        print(f"Валидация email работает: {type(e).__name__}")


if __name__ == "__main__":
    main()
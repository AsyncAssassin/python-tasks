"""
Примеры использования всех задач домашнего задания
"""

from task1 import fetch_posts, display_posts
from task2 import get_weather, display_weather
from task3 import create_post, display_created_post
from task4 import make_request, handle_status_code


def run_task1_example():
    print("=" * 80)
    print("ЗАДАНИЕ 1: Получение данных из публичного API")
    print("=" * 80)
    try:
        posts = fetch_posts(3)
        display_posts(posts)
    except Exception as e:
        print(f"Ошибка: {e}")


def run_task2_example():
    print("\n" + "=" * 80)
    print("ЗАДАНИЕ 2: Работа с параметрами запроса")
    print("=" * 80)
    try:
        weather_data = get_weather("Moscow")
        display_weather(weather_data)
    except Exception as e:
        print(f"Ошибка: {e}")


def run_task3_example():
    print("\n" + "=" * 80)
    print("ЗАДАНИЕ 3: Создание и обработка POST-запросов")
    print("=" * 80)
    try:
        post = create_post(
            title="Example Post",
            body="This is an example post created via API"
        )
        display_created_post(post)
    except Exception as e:
        print(f"Ошибка: {e}")


def run_task4_example():
    print("\n" + "=" * 80)
    print("ЗАДАНИЕ 4: Обработка ошибок и работа с данными")
    print("=" * 80)
    test_urls = [
        ("Успешный запрос", "https://jsonplaceholder.typicode.com/posts/1"),
        ("Ресурс не найден", "https://jsonplaceholder.typicode.com/posts/999999")
    ]

    for description, url in test_urls:
        print(f"\n{description}: {url}")
        print("-" * 60)
        response = make_request(url)
        if response:
            handle_status_code(response)


def main():
    run_task1_example()
    run_task2_example()
    run_task3_example()
    run_task4_example()


if __name__ == "__main__":
    main()

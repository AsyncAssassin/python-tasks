import requests
from typing import Optional

STATUS_MESSAGES = {
    200: "Успешный запрос",
    201: "Ресурс успешно создан",
    400: "Неверный запрос",
    401: "Требуется авторизация",
    403: "Доступ запрещён",
    404: "Ресурс не найден",
    500: "Внутренняя ошибка сервера",
    502: "Неверный шлюз",
    503: "Сервис недоступен"
}


def make_request(url: str, timeout: int = 15) -> Optional[requests.Response]:
    try:
        response = requests.get(url, timeout=timeout)
        return response
    except requests.Timeout:
        print(f"Ошибка: Превышено время ожидания ({timeout}s)")
        return None
    except requests.ConnectionError:
        print("Ошибка: Не удалось подключиться к серверу")
        return None
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None


def handle_status_code(response: requests.Response) -> None:
    status_code = response.status_code

    if status_code in STATUS_MESSAGES:
        message = STATUS_MESSAGES[status_code]
    else:
        message = f"Код состояния: {status_code}"

    print(f"HTTP статус: {status_code}")
    print(f"Сообщение: {message}")

    if 200 <= status_code < 300:
        try:
            data = response.json()
            if not data or data == {}:
                print("⚠️  Внимание: Сервер вернул пустой ответ (ресурс не найден)")
            else:
                print("✓ Запрос выполнен успешно")
        except ValueError:
            print("✓ Запрос выполнен успешно")
    elif 400 <= status_code < 500:
        print("✗ Ошибка клиента")
    elif 500 <= status_code < 600:
        print("✗ Ошибка сервера")


def main():
    print("=" * 80)
    print("ДЕМОНСТРАЦИЯ ОБРАБОТКИ HTTP СТАТУСОВ")
    print("=" * 80)

    test_cases = [
        ("Успешный GET запрос", "https://jsonplaceholder.typicode.com/posts/1"),
        ("Несуществующий пост (JSONPlaceholder возвращает {})",
         "https://jsonplaceholder.typicode.com/posts/99999"),
        ("Реальная 404 ошибка",
         "https://jsonplaceholder.typicode.com/nonexistent"),
        ("GitHub API - несуществующий пользователь (404)",
         "https://api.github.com/users/this_user_definitely_does_not_exist_12345"),
    ]

    for i, (description, url) in enumerate(test_cases, 1):
        print(f"\n{'─' * 80}")
        print(f"Тест {i}: {description}")
        print(f"URL: {url}")
        print('─' * 80)

        response = make_request(url)

        if response:
            handle_status_code(response)
        else:
            print("✗ Запрос не выполнен")

    print(f"\n{'=' * 80}")
    print("Тестирование завершено")
    print("=" * 80)


if __name__ == "__main__":
    main()
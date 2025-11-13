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


def make_request(url: str) -> Optional[requests.Response]:
    try:
        response = requests.get(url, timeout=10)
        return response
    except requests.RequestException as e:
        print(f"Ошибка соединения: {e}")
        return None


def handle_status_code(response: requests.Response) -> None:
    status_code = response.status_code

    if status_code in STATUS_MESSAGES:
        message = STATUS_MESSAGES[status_code]
    else:
        message = f"Неизвестный код состояния: {status_code}"

    print(f"HTTP статус: {status_code}")
    print(f"Сообщение: {message}")

    if 200 <= status_code < 300:
        try:
            data = response.json()
            if not data or data == {}:
                print("Ответ: Ресурс не найден (пустой ответ)")
            else:
                print("Запрос выполнен успешно")
        except ValueError:
            print("Запрос выполнен успешно")
    elif 400 <= status_code < 500:
        print("Ошибка клиента")
    elif 500 <= status_code < 600:
        print("Ошибка сервера")


def main():
    print("Тестирование обработки различных HTTP статусов\n")

    test_urls = [
        ("Успешный запрос", "https://jsonplaceholder.typicode.com/posts/1"),
        ("Несуществующий ресурс (JSONPlaceholder возвращает {})",
         "https://jsonplaceholder.typicode.com/posts/999999"),
        ("Некорректный эндпоинт",
         "https://jsonplaceholder.typicode.com/invalid-endpoint"),
        ("Тест с реальной 404 ошибкой",
         "https://api.github.com/users/thisdoesnotexist404404404"),
    ]

    for description, url in test_urls:
        print(f"\n{description}")
        print(f"URL: {url}")
        print("-" * 60)
        response = make_request(url)

        if response:
            handle_status_code(response)


if __name__ == "__main__":
    main()
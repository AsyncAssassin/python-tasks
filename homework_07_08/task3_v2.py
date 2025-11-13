import requests
from typing import Dict


def create_post(title: str, body: str, user_id: int = 1) -> Dict:
    url = "https://jsonplaceholder.typicode.com/posts"

    payload = {
        "title": title,
        "body": body,
        "userId": user_id
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()


def display_created_post(post: Dict) -> None:
    print(f"ID созданного поста: {post['id']}")
    print(f"Содержимое:")
    print(f"  Title: {post['title']}")
    print(f"  Body: {post['body']}")
    print(f"  User ID: {post['userId']}")


def main():
    title = input("Введите заголовок поста: ")
    body = input("Введите текст поста: ")

    try:
        post = create_post(title, body)
        display_created_post(post)
    except requests.RequestException as e:
        print(f"Ошибка при создании поста: {e}")


if __name__ == "__main__":
    main()

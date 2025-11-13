from api_client import JSONPlaceholderClient


def demo_posts():
    print("\n" + "=" * 80)
    print("ДЕМОНСТРАЦИЯ: Работа с постами")
    print("=" * 80)

    client = JSONPlaceholderClient()

    print("\n1. Получение всех постов (первые 3):")
    posts = client.get_posts()[:3]
    for post in posts:
        print(f"  - [{post.id}] {post.title}")

    print("\n2. Получение конкретного поста (ID=1):")
    post = client.get_post(1)
    if post:
        print(f"  Title: {post.title}")
        print(f"  Body: {post.body[:50]}...")

    print("\n3. Фильтрация постов по пользователю (userId=1):")
    user_posts = client.get_posts(user_id=1)
    print(f"  Найдено постов: {len(user_posts)}")

    print("\n4. Создание нового поста:")
    new_post = client.create_post(
        title="Тестовый пост",
        body="Это тестовое содержимое поста"
    )
    print(f"  Создан пост с ID: {new_post.id}")

    print("\n5. Обновление поста (PUT):")
    updated_post = client.update_post(
        post_id=1,
        title="Обновленный заголовок",
        body="Обновленное содержимое",
        user_id=1
    )
    print(f"  Обновлен пост ID: {updated_post.id}")

    print("\n6. Частичное обновление (PATCH):")
    patched_post = client.patch_post(1, title="Новый заголовок")
    print(f"  Обновлен заголовок поста ID: {patched_post.id}")

    print("\n7. Удаление поста:")
    success = client.delete_post(1)
    print(f"  Удаление {'успешно' if success else 'не удалось'}")


def demo_comments():
    print("\n" + "=" * 80)
    print("ДЕМОНСТРАЦИЯ: Работа с комментариями")
    print("=" * 80)

    client = JSONPlaceholderClient()

    print("\n1. Получение комментариев для поста (postId=1):")
    comments = client.get_comments(post_id=1)
    print(f"  Найдено комментариев: {len(comments)}")
    for comment in comments[:2]:
        print(f"  - [{comment.id}] {comment.name} ({comment.email})")


def demo_users():
    print("\n" + "=" * 80)
    print("ДЕМОНСТРАЦИЯ: Работа с пользователями")
    print("=" * 80)

    client = JSONPlaceholderClient()

    print("\n1. Получение всех пользователей:")
    users = client.get_users()
    for user in users[:3]:
        print(f"  - [{user.id}] {user.name} (@{user.username}) - {user.email}")

    print("\n2. Получение конкретного пользователя (ID=1):")
    user = client.get_user(1)
    if user:
        print(f"  Имя: {user.name}")
        print(f"  Email: {user.email}")
        print(f"  Город: {user.address.city}")
        print(f"  Компания: {user.company.name}")


def demo_albums_and_photos():
    print("\n" + "=" * 80)
    print("ДЕМОНСТРАЦИЯ: Работа с альбомами и фото")
    print("=" * 80)

    client = JSONPlaceholderClient()

    print("\n1. Получение альбомов пользователя (userId=1):")
    albums = client.get_albums(user_id=1)
    print(f"  Найдено альбомов: {len(albums)}")
    for album in albums[:3]:
        print(f"  - [{album.id}] {album.title}")

    print("\n2. Получение фото из альбома (albumId=1):")
    photos = client.get_photos(album_id=1)
    print(f"  Найдено фотографий: {len(photos)}")
    for photo in photos[:2]:
        print(f"  - [{photo.id}] {photo.title}")
        print(f"    URL: {photo.url}")


def demo_todos():
    print("\n" + "=" * 80)
    print("ДЕМОНСТРАЦИЯ: Работа с задачами")
    print("=" * 80)

    client = JSONPlaceholderClient()

    print("\n1. Получение задач пользователя (userId=1):")
    todos = client.get_todos(user_id=1)
    completed = sum(1 for todo in todos if todo.completed)
    print(f"  Всего задач: {len(todos)}")
    print(f"  Выполнено: {completed}")
    print(f"  Не выполнено: {len(todos) - completed}")

    print("\n  Первые 3 задачи:")
    for todo in todos[:3]:
        status = "✓" if todo.completed else "○"
        print(f"  {status} [{todo.id}] {todo.title}")


def main():
    print("\n" + "=" * 80)
    print("ПОЛНАЯ ДЕМОНСТРАЦИЯ JSONPlaceholder API CLIENT")
    print("=" * 80)

    try:
        demo_posts()
        demo_comments()
        demo_users()
        demo_albums_and_photos()
        demo_todos()

        print("\n" + "=" * 80)
        print("Демонстрация завершена успешно!")
        print("=" * 80 + "\n")
    except Exception as e:
        print(f"\n✗ Ошибка при выполнении демонстрации: {e}")


if __name__ == "__main__":
    main()
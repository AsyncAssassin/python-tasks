import json
from datetime import date, datetime


def test_task1_basic():
    """Задание 1: Базовое обращение"""
    payload = {
        "surname": "Иванов",
        "name": "Иван",
        "birth_date": "1990-05-15",
        "phone": "+79991234567",
        "email": "ivanov@example.com"
    }
    print("Задание 1 - Базовое обращение:")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    print()


def test_task2_with_issue():
    """Задание 2: Обращение с проблемой"""
    payload = {
        "surname": "Петров",
        "name": "Петр",
        "birth_date": "1985-03-20",
        "phone": "+79167654321",
        "email": "petrov@example.com",
        "issue_reason": "нет доступа к сети",
        "issue_datetime": datetime.now().isoformat()
    }
    print("Задание 2 - Обращение с проблемой:")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    print()


def test_task3_multiple_issues():
    """Задание 3: Обращение с несколькими проблемами"""
    payload = {
        "surname": "Сидоров",
        "name": "Сидор",
        "birth_date": "1995-07-10",
        "phone": "+79261234567",
        "email": "sidorov@example.com",
        "issue_reasons": [
            "нет доступа к сети",
            "не работает телефон",
            "не приходят письма"
        ],
        "issue_datetime": datetime.now().isoformat()
    }
    print("Задание 3 - Обращение с несколькими проблемами:")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    print()


def test_validation_errors():
    """Примеры невалидных данных"""

    invalid_cases = [
        {
            "description": "Имя с маленькой буквы",
            "payload": {
                "surname": "Иванов",
                "name": "иван",
                "birth_date": "1990-05-15",
                "phone": "+79991234567",
                "email": "test@example.com"
            }
        },
        {
            "description": "Фамилия с латиницей",
            "payload": {
                "surname": "Ivanov",
                "name": "Иван",
                "birth_date": "1990-05-15",
                "phone": "+79991234567",
                "email": "test@example.com"
            }
        },
        {
            "description": "Невалидный телефон",
            "payload": {
                "surname": "Иванов",
                "name": "Иван",
                "birth_date": "1990-05-15",
                "phone": "123",
                "email": "test@example.com"
            }
        },
        {
            "description": "Дата рождения в будущем",
            "payload": {
                "surname": "Иванов",
                "name": "Иван",
                "birth_date": "2030-05-15",
                "phone": "+79991234567",
                "email": "test@example.com"
            }
        }
    ]

    print("Примеры невалидных данных (должны вызвать ошибки):")
    for case in invalid_cases:
        print(f"\n{case['description']}:")
        print(json.dumps(case['payload'], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    print("=" * 80)
    print("ПРИМЕРЫ ЗАПРОСОВ ДЛЯ ТЕСТИРОВАНИЯ API")
    print("=" * 80)
    print()

    test_task1_basic()
    test_task2_with_issue()
    test_task3_multiple_issues()
    test_validation_errors()

    print("\n" + "=" * 80)
    print("КОМАНДЫ ДЛЯ ЗАПУСКА:")
    print("=" * 80)
    print()
    print("1. Запуск сервера:")
    print("   uvicorn main:app --reload")
    print()
    print("2. Тестовый запрос (Задание 1):")
    print("   curl -X POST http://localhost:8000/subscriber \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{")
    print("       \"surname\": \"Иванов\",")
    print("       \"name\": \"Иван\",")
    print("       \"birth_date\": \"1990-05-15\",")
    print("       \"phone\": \"+79991234567\",")
    print("       \"email\": \"ivanov@example.com\"")
    print("     }'")
    print()
    print("3. Документация API:")
    print("   http://localhost:8000/docs")
    print()
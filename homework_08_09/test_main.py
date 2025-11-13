from datetime import date, datetime
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from main import app, DATA_FILE

client = TestClient(app)


@pytest.fixture(autouse=True)
def cleanup_data_file():
    yield
    if DATA_FILE.exists():
        DATA_FILE.unlink()


class TestTask1BasicSubscriber:

    def test_create_subscriber_success(self):
        response = client.post("/subscriber", json={
            "surname": "Иванов",
            "name": "Иван",
            "birth_date": "1990-05-15",
            "phone": "+79991234567",
            "email": "ivanov@example.com"
        })

        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "Обращение успешно сохранено"
        assert data["data"]["surname"] == "Иванов"
        assert data["data"]["name"] == "Иван"
        assert "created_at" in data["data"]

    def test_surname_not_capitalized(self):
        response = client.post("/subscriber", json={
            "surname": "иванов",
            "name": "Иван",
            "birth_date": "1990-05-15",
            "phone": "+79991234567",
            "email": "test@example.com"
        })

        assert response.status_code == 422
        assert "Должно начинаться с заглавной буквы" in response.text

    def test_name_not_capitalized(self):
        response = client.post("/subscriber", json={
            "surname": "Иванов",
            "name": "иван",
            "birth_date": "1990-05-15",
            "phone": "+79991234567",
            "email": "test@example.com"
        })

        assert response.status_code == 422
        assert "Должно начинаться с заглавной буквы" in response.text

    def test_surname_latin_characters(self):
        response = client.post("/subscriber", json={
            "surname": "Ivanov",
            "name": "Иван",
            "birth_date": "1990-05-15",
            "phone": "+79991234567",
            "email": "test@example.com"
        })

        assert response.status_code == 422
        assert "Может содержать только кириллицу" in response.text

    def test_name_latin_characters(self):
        response = client.post("/subscriber", json={
            "surname": "Иванов",
            "name": "Ivan",
            "birth_date": "1990-05-15",
            "phone": "+79991234567",
            "email": "test@example.com"
        })

        assert response.status_code == 422
        assert "Может содержать только кириллицу" in response.text

    def test_surname_with_hyphen(self):
        response = client.post("/subscriber", json={
            "surname": "Иванов-Петров",
            "name": "Иван",
            "birth_date": "1990-05-15",
            "phone": "+79991234567",
            "email": "test@example.com"
        })

        assert response.status_code == 201

    def test_invalid_phone_format(self):
        response = client.post("/subscriber", json={
            "surname": "Иванов",
            "name": "Иван",
            "birth_date": "1990-05-15",
            "phone": "123",
            "email": "test@example.com"
        })

        assert response.status_code == 422

    def test_invalid_email(self):
        response = client.post("/subscriber", json={
            "surname": "Иванов",
            "name": "Иван",
            "birth_date": "1990-05-15",
            "phone": "+79991234567",
            "email": "not-an-email"
        })

        assert response.status_code == 422

    def test_future_birth_date(self):
        future_date = date.today().replace(year=date.today().year + 1)
        response = client.post("/subscriber", json={
            "surname": "Иванов",
            "name": "Иван",
            "birth_date": future_date.isoformat(),
            "phone": "+79991234567",
            "email": "test@example.com"
        })

        assert response.status_code == 422
        assert "Дата рождения не может быть в будущем" in response.text

    def test_missing_required_field(self):
        response = client.post("/subscriber", json={
            "surname": "Иванов",
            "birth_date": "1990-05-15",
            "phone": "+79991234567",
            "email": "test@example.com"
        })

        assert response.status_code == 422


class TestTask2SubscriberWithIssue:

    def test_create_subscriber_with_issue_success(self):
        response = client.post("/subscriber/with-issue", json={
            "surname": "Петров",
            "name": "Петр",
            "birth_date": "1985-03-20",
            "phone": "+79167654321",
            "email": "petrov@example.com",
            "issue_reason": "нет доступа к сети",
            "issue_datetime": datetime.now().isoformat()
        })

        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "Обращение с проблемой успешно сохранено"
        assert data["data"]["issue_reason"] == "нет доступа к сети"
        assert "issue_datetime" in data["data"]

    def test_missing_issue_reason(self):
        response = client.post("/subscriber/with-issue", json={
            "surname": "Петров",
            "name": "Петр",
            "birth_date": "1985-03-20",
            "phone": "+79167654321",
            "email": "petrov@example.com",
            "issue_datetime": datetime.now().isoformat()
        })

        assert response.status_code == 400
        assert "Необходимо указать причину обращения" in response.text

    def test_missing_issue_datetime(self):
        response = client.post("/subscriber/with-issue", json={
            "surname": "Петров",
            "name": "Петр",
            "birth_date": "1985-03-20",
            "phone": "+79167654321",
            "email": "petrov@example.com",
            "issue_reason": "нет доступа к сети"
        })

        assert response.status_code == 400
        assert "время обнаружения проблемы" in response.text

    def test_invalid_issue_reason(self):
        response = client.post("/subscriber/with-issue", json={
            "surname": "Петров",
            "name": "Петр",
            "birth_date": "1985-03-20",
            "phone": "+79167654321",
            "email": "petrov@example.com",
            "issue_reason": "неизвестная проблема",
            "issue_datetime": datetime.now().isoformat()
        })

        assert response.status_code == 422

    def test_all_issue_types(self):
        issue_types = [
            "нет доступа к сети",
            "не работает телефон",
            "не приходят письма"
        ]

        for issue_type in issue_types:
            response = client.post("/subscriber/with-issue", json={
                "surname": "Тестов",
                "name": "Тест",
                "birth_date": "1990-01-01",
                "phone": "+79991234567",
                "email": f"test_{issue_type.replace(' ', '_')}@example.com",
                "issue_reason": issue_type,
                "issue_datetime": datetime.now().isoformat()
            })

            assert response.status_code == 201
            assert issue_type in response.json()["data"]["issue_reason"]


class TestTask3SubscriberWithMultipleIssues:

    def test_create_subscriber_with_multiple_issues_success(self):
        response = client.post("/subscriber/with-multiple-issues", json={
            "surname": "Сидоров",
            "name": "Сидор",
            "birth_date": "1995-07-10",
            "phone": "+79261234567",
            "email": "sidorov@example.com",
            "issue_reasons": [
                "нет доступа к сети",
                "не работает телефон"
            ],
            "issue_datetime": datetime.now().isoformat()
        })

        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "Обращение с множественными проблемами успешно сохранено"
        assert len(data["data"]["issue_reasons"]) == 2
        assert "нет доступа к сети" in data["data"]["issue_reasons"]
        assert "не работает телефон" in data["data"]["issue_reasons"]

    def test_all_three_issues(self):
        response = client.post("/subscriber/with-multiple-issues", json={
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
        })

        assert response.status_code == 201
        assert len(response.json()["data"]["issue_reasons"]) == 3

    def test_missing_issue_reasons(self):
        response = client.post("/subscriber/with-multiple-issues", json={
            "surname": "Сидоров",
            "name": "Сидор",
            "birth_date": "1995-07-10",
            "phone": "+79261234567",
            "email": "sidorov@example.com",
            "issue_datetime": datetime.now().isoformat()
        })

        assert response.status_code == 400

    def test_empty_issue_reasons_list(self):
        response = client.post("/subscriber/with-multiple-issues", json={
            "surname": "Сидоров",
            "name": "Сидор",
            "birth_date": "1995-07-10",
            "phone": "+79261234567",
            "email": "sidorov@example.com",
            "issue_reasons": [],
            "issue_datetime": datetime.now().isoformat()
        })

        assert response.status_code == 422
        assert "не может быть пустым" in response.text


class TestGetSubscribers:

    def test_get_empty_subscribers(self):
        response = client.get("/subscribers")

        assert response.status_code == 200
        assert response.json() == {"subscribers": []}

    def test_get_subscribers_after_creation(self):
        client.post("/subscriber", json={
            "surname": "Иванов",
            "name": "Иван",
            "birth_date": "1990-05-15",
            "phone": "+79991234567",
            "email": "ivanov@example.com"
        })

        client.post("/subscriber/with-issue", json={
            "surname": "Петров",
            "name": "Петр",
            "birth_date": "1985-03-20",
            "phone": "+79167654321",
            "email": "petrov@example.com",
            "issue_reason": "нет доступа к сети",
            "issue_datetime": datetime.now().isoformat()
        })

        response = client.get("/subscribers")

        assert response.status_code == 200
        subscribers = response.json()["subscribers"]
        assert len(subscribers) == 2
        assert subscribers[0]["surname"] == "Иванов"
        assert subscribers[1]["surname"] == "Петров"


class TestHealthCheck:

    def test_health_check(self):
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
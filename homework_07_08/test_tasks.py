import pytest
import requests
from unittest.mock import patch, Mock
from task1 import fetch_posts, display_posts
from task3 import create_post
from task4 import handle_status_code


class TestTask1:
    @patch('task1.requests.get')
    def test_fetch_posts(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = [
            {"id": 1, "title": "Test", "body": "Body"},
            {"id": 2, "title": "Test2", "body": "Body2"}
        ]
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        posts = fetch_posts(2)
        assert len(posts) == 2
        assert posts[0]["title"] == "Test"


class TestTask3:
    @patch('task3.requests.post')
    def test_create_post(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": 101,
            "title": "Test Title",
            "body": "Test Body",
            "userId": 1
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        post = create_post("Test Title", "Test Body")
        assert post["id"] == 101
        assert post["title"] == "Test Title"


class TestTask4:
    def test_handle_status_code_200(self, capsys):
        mock_response = Mock()
        mock_response.status_code = 200

        handle_status_code(mock_response)
        captured = capsys.readouterr()
        assert "Успешный запрос" in captured.out
        assert "Запрос выполнен успешно" in captured.out

    def test_handle_status_code_404(self, capsys):
        mock_response = Mock()
        mock_response.status_code = 404

        handle_status_code(mock_response)
        captured = capsys.readouterr()
        assert "Ресурс не найден" in captured.out
        assert "Ошибка клиента" in captured.out

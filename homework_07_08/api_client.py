import requests
from typing import List, Optional, Dict, Any
from models import Post, Comment, Album, Photo, Todo, User


class JSONPlaceholderClient:
    BASE_URL = "https://jsonplaceholder.typicode.com"

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json; charset=UTF-8"
        })

    def _request(
            self,
            method: str,
            endpoint: str,
            data: Optional[Dict[str, Any]] = None,
            params: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        url = f"{self.BASE_URL}{endpoint}"
        response = self.session.request(
            method=method,
            url=url,
            json=data,
            params=params,
            timeout=self.timeout
        )
        return response

    def get_posts(self, user_id: Optional[int] = None) -> List[Post]:
        params = {"userId": user_id} if user_id else None
        response = self._request("GET", "/posts", params=params)
        response.raise_for_status()
        return [Post(**post) for post in response.json()]

    def get_post(self, post_id: int) -> Optional[Post]:
        response = self._request("GET", f"/posts/{post_id}")
        response.raise_for_status()
        data = response.json()
        return Post(**data) if data else None

    def create_post(self, title: str, body: str, user_id: int = 1) -> Post:
        data = {"title": title, "body": body, "userId": user_id}
        response = self._request("POST", "/posts", data=data)
        response.raise_for_status()
        return Post(**response.json())

    def update_post(self, post_id: int, title: str, body: str, user_id: int) -> Post:
        data = {"id": post_id, "title": title, "body": body, "userId": user_id}
        response = self._request("PUT", f"/posts/{post_id}", data=data)
        response.raise_for_status()
        return Post(**response.json())

    def patch_post(self, post_id: int, **kwargs) -> Post:
        response = self._request("PATCH", f"/posts/{post_id}", data=kwargs)
        response.raise_for_status()
        return Post(**response.json())

    def delete_post(self, post_id: int) -> bool:
        response = self._request("DELETE", f"/posts/{post_id}")
        return response.status_code == 200

    def get_comments(self, post_id: Optional[int] = None) -> List[Comment]:
        if post_id:
            endpoint = f"/posts/{post_id}/comments"
        else:
            endpoint = "/comments"
        response = self._request("GET", endpoint)
        response.raise_for_status()
        return [Comment(**comment) for comment in response.json()]

    def get_users(self) -> List[User]:
        response = self._request("GET", "/users")
        response.raise_for_status()
        return [User(**user) for user in response.json()]

    def get_user(self, user_id: int) -> Optional[User]:
        response = self._request("GET", f"/users/{user_id}")
        response.raise_for_status()
        data = response.json()
        return User(**data) if data else None

    def get_albums(self, user_id: Optional[int] = None) -> List[Album]:
        params = {"userId": user_id} if user_id else None
        response = self._request("GET", "/albums", params=params)
        response.raise_for_status()
        return [Album(**album) for album in response.json()]

    def get_photos(self, album_id: Optional[int] = None) -> List[Photo]:
        params = {"albumId": album_id} if album_id else None
        response = self._request("GET", "/photos", params=params)
        response.raise_for_status()
        return [Photo(**photo) for photo in response.json()]

    def get_todos(self, user_id: Optional[int] = None) -> List[Todo]:
        params = {"userId": user_id} if user_id else None
        response = self._request("GET", "/todos", params=params)
        response.raise_for_status()
        return [Todo(**todo) for todo in response.json()]
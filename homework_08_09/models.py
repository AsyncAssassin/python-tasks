from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class IssueType(str, Enum):
    NO_INTERNET = "нет доступа к сети"
    PHONE_NOT_WORKING = "не работает телефон"
    NO_EMAILS = "не приходят письма"


class SubscriberRequest(BaseModel):
    surname: str = Field(..., min_length=2, max_length=50)
    name: str = Field(..., min_length=2, max_length=50)
    birth_date: date
    phone: str = Field(..., pattern=r"^\+?[0-9]{10,15}$")
    email: EmailStr
    issue_reason: Optional[IssueType] = None
    issue_datetime: Optional[datetime] = None
    issue_reasons: Optional[list[IssueType]] = None

    @field_validator("surname", "name")
    @classmethod
    def validate_cyrillic_capitalized(cls, v: str) -> str:
        if not v:
            raise ValueError("Поле не может быть пустым")

        if not v[0].isupper():
            raise ValueError("Должно начинаться с заглавной буквы")

        if not all(c.isalpha() or c.isspace() or c == "-" for c in v):
            raise ValueError("Может содержать только буквы, пробелы и дефисы")

        if not all(c in "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя -" for c in v):
            raise ValueError("Может содержать только кириллицу")

        return v

    @field_validator("birth_date")
    @classmethod
    def validate_birth_date(cls, v: date) -> date:
        if v > date.today():
            raise ValueError("Дата рождения не может быть в будущем")

        age = (date.today() - v).days // 365
        if age > 150:
            raise ValueError("Некорректная дата рождения")

        return v

    @field_validator("issue_datetime")
    @classmethod
    def validate_issue_datetime(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v and v > datetime.now():
            raise ValueError("Дата обнаружения проблемы не может быть в будущем")
        return v

    @field_validator("issue_reasons")
    @classmethod
    def validate_issue_reasons_not_empty(cls, v: Optional[list[IssueType]]) -> Optional[list[IssueType]]:
        if v is not None and len(v) == 0:
            raise ValueError("Список причин не может быть пустым, если передан")
        return v
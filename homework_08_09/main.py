import json
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

from models import SubscriberRequest

app = FastAPI(title="Subscriber Service", version="1.0.0")

DATA_FILE = Path(__file__).parent / "subscribers.json"


def save_subscriber(data: dict[str, Any]) -> None:
    subscribers = []

    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                subscribers = json.load(f)
            except json.JSONDecodeError:
                subscribers = []

    subscribers.append(data)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(subscribers, f, ensure_ascii=False, indent=2, default=str)


@app.post("/subscriber", status_code=status.HTTP_201_CREATED)
async def create_subscriber(request: SubscriberRequest) -> JSONResponse:
    try:
        subscriber_data = {
            "surname": request.surname,
            "name": request.name,
            "birth_date": request.birth_date.isoformat(),
            "phone": request.phone,
            "email": request.email,
            "created_at": datetime.now().isoformat()
        }

        save_subscriber(subscriber_data)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Обращение успешно сохранено", "data": subscriber_data}
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при сохранении данных: {str(e)}"
        )


@app.post("/subscriber/with-issue", status_code=status.HTTP_201_CREATED)
async def create_subscriber_with_issue(request: SubscriberRequest) -> JSONResponse:
    if not request.issue_reason or not request.issue_datetime:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Необходимо указать причину обращения и время обнаружения проблемы"
        )

    try:
        subscriber_data = {
            "surname": request.surname,
            "name": request.name,
            "birth_date": request.birth_date.isoformat(),
            "phone": request.phone,
            "email": request.email,
            "issue_reason": request.issue_reason.value,
            "issue_datetime": request.issue_datetime.isoformat(),
            "created_at": datetime.now().isoformat()
        }

        save_subscriber(subscriber_data)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Обращение с проблемой успешно сохранено", "data": subscriber_data}
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при сохранении данных: {str(e)}"
        )


@app.post("/subscriber/with-multiple-issues", status_code=status.HTTP_201_CREATED)
async def create_subscriber_with_multiple_issues(request: SubscriberRequest) -> JSONResponse:
    if not request.issue_reasons or not request.issue_datetime:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Необходимо указать причины обращения и время обнаружения проблемы"
        )

    try:
        subscriber_data = {
            "surname": request.surname,
            "name": request.name,
            "birth_date": request.birth_date.isoformat(),
            "phone": request.phone,
            "email": request.email,
            "issue_reasons": [reason.value for reason in request.issue_reasons],
            "issue_datetime": request.issue_datetime.isoformat(),
            "created_at": datetime.now().isoformat()
        }

        save_subscriber(subscriber_data)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Обращение с множественными проблемами успешно сохранено", "data": subscriber_data}
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при сохранении данных: {str(e)}"
        )


@app.get("/subscribers")
async def get_all_subscribers() -> JSONResponse:
    if not DATA_FILE.exists():
        return JSONResponse(content={"subscribers": []})

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            subscribers = json.load(f)
            return JSONResponse(content={"subscribers": subscribers})
        except json.JSONDecodeError:
            return JSONResponse(content={"subscribers": []})


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
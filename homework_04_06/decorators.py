import functools
from datetime import datetime


def log_operation(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {func.__name__}")

        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            print(f"[{timestamp}] Ошибка: {e}")
            raise

    return wrapper
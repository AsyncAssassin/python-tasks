"""
Тесты для FastAPI калькулятора
"""

import requests
import sys

BASE_URL = "http://127.0.0.1:8000"


def test_add():
    """Тест сложения"""
    print("Тестирование сложения...")
    response = requests.post(f"{BASE_URL}/add", json={"a": 10, "b": 5})
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 15
    print(f"Сложение: {data['a']} + {data['b']} = {data['result']}")


def test_subtract():
    """Тест вычитания"""
    print("\n Тестирование вычитания...")
    response = requests.post(f"{BASE_URL}/subtract", json={"a": 20, "b": 7})
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 13
    print(f" Вычитание: {data['a']} - {data['b']} = {data['result']}")


def test_multiply():
    """Тест умножения"""
    print("\n Тестирование умножения...")
    response = requests.post(f"{BASE_URL}/multiply", json={"a": 6, "b": 7})
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 42
    print(f" Умножение: {data['a']} * {data['b']} = {data['result']}")


def test_divide():
    """Тест деления"""
    print("\n Тестирование деления...")
    response = requests.post(f"{BASE_URL}/divide", json={"a": 20, "b": 4})
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 5.0
    print(f" Деление: {data['a']} / {data['b']} = {data['result']}")


def test_divide_by_zero():
    """Тест деления на ноль"""
    print("\n Тестирование деления на ноль...")
    response = requests.post(f"{BASE_URL}/divide", json={"a": 10, "b": 0})
    assert response.status_code == 400
    assert "Деление на ноль" in response.json()["detail"]
    print(" Деление на ноль корректно обработано")


def test_create_expression():
    """Тест создания простого выражения"""
    print("\n Тестирование создания выражения...")
    response = requests.post(f"{BASE_URL}/create-expression",
                             json={"a": 15, "op": "+", "b": 7})
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 22
    print(f" Выражение: {data['expression']} = {data['result']}")


def test_evaluate_simple_expression():
    """Тест вычисления простого сложного выражения"""
    print("\n Тестирование простого выражения...")
    response = requests.post(f"{BASE_URL}/evaluate-complex",
                             json={"expression": "(2+3)*4"})
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 20
    print(f" Выражение: {data['expression']} = {data['result']}")


def test_evaluate_complex_expression():
    """Тест вычисления сложного выражения"""
    print("\n Тестирование сложного выражения...")
    expression = "(10+5)*2 + (20-5)/(3)"
    response = requests.post(f"{BASE_URL}/evaluate-complex",
                             json={"expression": expression})
    assert response.status_code == 200
    data = response.json()
    expected = (10 + 5) * 2 + (20 - 5) / (3)
    assert abs(data["result"] - expected) < 0.0001
    print(f" Выражение: {data['expression']} = {data['result']}")


def test_expression_management():
    """Тест управления текущим выражением"""
    print("\n Тестирование управления выражением...")

    expression = "(8+2)*5"
    response = requests.post(f"{BASE_URL}/expression/set",
                             json={"expression": expression})
    assert response.status_code == 200
    print(f"   1. Выражение установлено: {expression}")

    response = requests.get(f"{BASE_URL}/expression/current")
    assert response.status_code == 200
    data = response.json()
    assert data["expression"] == expression
    print(f"   2. Текущее выражение: {data['expression']}")

    response = requests.post(f"{BASE_URL}/expression/execute")
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 50
    print(f"   3. Результат выполнения: {data['result']}")

    response = requests.delete(f"{BASE_URL}/expression/clear")
    assert response.status_code == 200
    print("   4. Выражение очищено")

    response = requests.get(f"{BASE_URL}/expression/current")
    data = response.json()
    assert data["expression"] is None
    print(" Управление выражением работает корректно")


def test_complex_mathematical_expression():
    """Тест сложного математического выражения без скобок"""
    print("\n Тестирование выражения с приоритетом операций...")
    expression = "2+3*4-5/2"
    response = requests.post(f"{BASE_URL}/evaluate-complex",
                             json={"expression": expression})
    assert response.status_code == 200
    data = response.json()
    expected = 2 + 3 * 4 - 5 / 2  # = 2 + 12 - 2.5 = 11.5
    assert data["result"] == expected
    print(f" Выражение: {data['expression']} = {data['result']}")


def run_all_tests():
    """Запуск всех тестов"""
    print("=" * 60)
    print(" ЗАПУСК ТЕСТОВ КАЛЬКУЛЯТОРА")
    print("=" * 60)

    try:
        # Проверка доступности сервера
        response = requests.get(BASE_URL, timeout=2)
        if response.status_code != 200:
            print(" Сервер не отвечает. Запустите приложение: python calculator_api.py")
            return False
    except requests.exceptions.ConnectionError:
        print(" Не удается подключиться к серверу.")
        print("   Убедитесь, что приложение запущено: python calculator_api.py")
        return False

    tests = [
        test_add,
        test_subtract,
        test_multiply,
        test_divide,
        test_divide_by_zero,
        test_create_expression,
        test_evaluate_simple_expression,
        test_evaluate_complex_expression,
        test_expression_management,
        test_complex_mathematical_expression,
    ]

    failed = 0
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f" ТЕСТ ПРОВАЛЕН: {test.__name__}")
            print(f"   Ошибка: {e}")
            failed += 1
        except Exception as e:
            print(f" ОШИБКА В ТЕСТЕ: {test.__name__}")
            print(f"   {type(e).__name__}: {e}")
            failed += 1

    print("\n" + "=" * 60)
    if failed == 0:
        print("ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    else:
        print(f"ПРОВАЛЕНО ТЕСТОВ: {failed}/{len(tests)}")
    print("=" * 60)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
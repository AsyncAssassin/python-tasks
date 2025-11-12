from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re

app = FastAPI(title="Calculator API", description="Простой калькулятор на FastAPI")


# Модели данных
class Operation(BaseModel):
    """Модель для базовых операций с двумя числами"""
    a: float
    b: float


class ExpressionCreate(BaseModel):
    """Модель для создания выражения с операцией"""
    a: float
    op: str  # '+', '-', '*', '/'
    b: float


class ComplexExpression(BaseModel):
    """Модель для сложных выражений в виде строки"""
    expression: str


current_expression = {"value": None}

@app.post("/add", tags=["Базовые операции"])
async def add(operation: Operation):
    """Сложение двух чисел"""
    result = operation.a + operation.b
    return {"operation": "addition", "a": operation.a, "b": operation.b, "result": result}


@app.post("/subtract", tags=["Базовые операции"])
async def subtract(operation: Operation):
    """Вычитание двух чисел"""
    result = operation.a - operation.b
    return {"operation": "subtraction", "a": operation.a, "b": operation.b, "result": result}


@app.post("/multiply", tags=["Базовые операции"])
async def multiply(operation: Operation):
    """Умножение двух чисел"""
    result = operation.a * operation.b
    return {"operation": "multiplication", "a": operation.a, "b": operation.b, "result": result}


@app.post("/divide", tags=["Базовые операции"])
async def divide(operation: Operation):
    """Деление двух чисел"""
    if operation.b == 0:
        raise HTTPException(status_code=400, detail="Деление на ноль невозможно")
    result = operation.a / operation.b
    return {"operation": "division", "a": operation.a, "b": operation.b, "result": result}

@app.post("/create-expression", tags=["Построение выражения"])
async def create_expression(expr: ExpressionCreate):
    """
    Создает простое выражение вида 'a op b'
    где op может быть: '+', '-', '*', '/'
    """
    operations = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b if b != 0 else None
    }

    if expr.op not in operations:
        raise HTTPException(status_code=400, detail=f"Неизвестная операция: {expr.op}")

    if expr.op == '/' and expr.b == 0:
        raise HTTPException(status_code=400, detail="Деление на ноль невозможно")

    result = operations[expr.op](expr.a, expr.b)
    expression_str = f"({expr.a} {expr.op} {expr.b})"

    return {
        "expression": expression_str,
        "result": result,
        "components": {"a": expr.a, "op": expr.op, "b": expr.b}
    }


@app.post("/evaluate-complex", tags=["Сложные выражения"])
async def evaluate_complex(expr: ComplexExpression):
    """
    Вычисляет сложное математическое выражение вида (a+b)*c + (d-e)/(f-g)
    Парсит строку, расставляет правильный порядок операций и вычисляет результат.

    Примеры:
    - "(2+3)*4"
    - "(10+5)*2 + (20-5)/(3)"
    - "2+3*4-5/2"
    """
    try:
        expression = expr.expression.replace(" ", "")

        if not re.match(r'^[\d+\-*/().]+$', expression):
            raise HTTPException(
                status_code=400,
                detail="Выражение содержит недопустимые символы. Используйте только цифры и операции +, -, *, /, ()"
            )

        if expression.count('(') != expression.count(')'):
            raise HTTPException(status_code=400, detail="Несбалансированные скобки")

        result = eval(expression, {"__builtins__": {}}, {})

        return {
            "expression": expr.expression,
            "result": result,
            "success": True
        }

    except ZeroDivisionError:
        raise HTTPException(status_code=400, detail="Деление на ноль в выражении")
    except SyntaxError:
        raise HTTPException(status_code=400, detail="Синтаксическая ошибка в выражении")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка при вычислении: {str(e)}")

@app.post("/expression/set", tags=["Управление выражением"])
async def set_expression(expr: ComplexExpression):
    """
    Устанавливает текущее выражение для последующего вычисления
    """
    current_expression["value"] = expr.expression
    return {
        "message": "Выражение установлено",
        "expression": expr.expression
    }


@app.get("/expression/current", tags=["Управление выражением"])
async def get_current_expression():
    """
    Возвращает текущее сохраненное выражение (Пункт 3)
    """
    if current_expression["value"] is None:
        return {"expression": None, "message": "Выражение не установлено"}

    return {
        "expression": current_expression["value"],
        "status": "ready_to_evaluate"
    }


@app.post("/expression/execute", tags=["Управление выражением"])
async def execute_current_expression():
    """
    Выполняет текущее сохраненное выражение и возвращает результат (Пункт 4)
    """
    if current_expression["value"] is None:
        raise HTTPException(status_code=400, detail="Выражение не установлено. Используйте /expression/set")

    try:
        expression = current_expression["value"].replace(" ", "")

        if not re.match(r'^[\d+\-*/().]+$', expression):
            raise HTTPException(status_code=400, detail="Недопустимые символы в выражении")

        result = eval(expression, {"__builtins__": {}}, {})

        return {
            "expression": current_expression["value"],
            "result": result,
            "success": True
        }

    except ZeroDivisionError:
        raise HTTPException(status_code=400, detail="Деление на ноль в выражении")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка при вычислении: {str(e)}")


@app.delete("/expression/clear", tags=["Управление выражением"])
async def clear_expression():
    """Очищает текущее выражение"""
    current_expression["value"] = None
    return {"message": "Выражение очищено"}


# Корневой эндпоинт
@app.get("/")
async def root():
    """Информация о API"""
    return {
        "message": "FastAPI Calculator API",
        "version": "1.0",
        "endpoints": {
            "basic": ["/add", "/subtract", "/multiply", "/divide"],
            "complex": ["/evaluate-complex"],
            "management": ["/expression/set", "/expression/current", "/expression/execute"]
        },
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
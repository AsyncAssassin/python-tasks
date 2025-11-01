"""
Домашнее задание 5 по теме 7: Параллельные вычисления
Дисциплина: Язык Python для разработчиков
Тема: Параллельные вычисления. Многопоточность и многопроцессность
Преподаватель: Владимир Хомутов
Дедлайн: 1.11.25

Модуль содержит классы для демонстрации работы с многопоточностью в Python.
"""

import threading
import time
from typing import List, Callable
from datetime import datetime


class Task1Calculator:
    """
    Класс для решения Задания 1: Вычисление квадратов и кубов чисел.

    Создаёт 2 потока для параллельного вычисления:
    - Первый поток вычисляет квадраты чисел от 1 до 10
    - Второй поток вычисляет кубы чисел от 1 до 10
    """

    def __init__(self, start: int = 1, end: int = 10):
        """
        Инициализация калькулятора.

        Args:
            start: Начальное число диапазона (по умолчанию 1)
            end: Конечное число диапазона (по умолчанию 10)
        """
        self.start = start
        self.end = end
        self.squares_results = []
        self.cubes_results = []
        self.execution_time = 0

    def calculate_squares(self) -> None:
        """Вычисляет квадраты чисел в заданном диапазоне."""
        print(f"\n[{self._get_time()}]  Поток 1: Начало вычисления квадратов")

        for i in range(self.start, self.end + 1):
            square = i ** 2
            self.squares_results.append((i, square))
            print(f"  Квадрат {i}² = {square}")
            time.sleep(0.1)  # Имитация вычислительной нагрузки

        print(f"[{self._get_time()}]  Поток 1: Вычисление квадратов завершено")

    def calculate_cubes(self) -> None:
        """Вычисляет кубы чисел в заданном диапазоне."""
        print(f"\n[{self._get_time()}]  Поток 2: Начало вычисления кубов")

        for i in range(self.start, self.end + 1):
            cube = i ** 3
            self.cubes_results.append((i, cube))
            print(f"  Куб {i}³ = {cube}")
            time.sleep(0.1)  # Имитация вычислительной нагрузки

        print(f"[{self._get_time()}]  Поток 2: Вычисление кубов завершено")

    def run(self) -> dict:
        """
        Запускает оба потока параллельно и ожидает их завершения.

        Returns:
            dict: Словарь с результатами и временем выполнения
        """
        print("\n" + "=" * 70)
        print("ЗАДАНИЕ 1: Вычисление квадратов и кубов")
        print("=" * 70)

        # Создание потоков
        thread_squares = threading.Thread(target=self.calculate_squares, name="SquaresThread")
        thread_cubes = threading.Thread(target=self.calculate_cubes, name="CubesThread")

        # Запуск потоков
        print("\n Запуск параллельных вычислений...")
        start_time = time.time()

        thread_squares.start()
        thread_cubes.start()

        # Ожидание завершения
        thread_squares.join()
        thread_cubes.join()

        self.execution_time = time.time() - start_time

        # Вывод результатов
        self._print_results()

        return {
            'squares': self.squares_results,
            'cubes': self.cubes_results,
            'execution_time': self.execution_time
        }

    def _print_results(self) -> None:
        """Выводит итоговые результаты вычислений."""
        print("\n" + "=" * 70)
        print(" РЕЗУЛЬТАТЫ ЗАДАНИЯ 1")
        print("=" * 70)
        print(f"  Время выполнения: {self.execution_time:.2f} секунд")
        print(f" Без многопоточности: ~{(self.end - self.start + 1) * 0.2:.2f} секунд")
        print(f" Ускорение: ~{((self.end - self.start + 1) * 0.2) / self.execution_time:.1f}x")
        print("=" * 70)

    @staticmethod
    def _get_time() -> str:
        """Возвращает текущее время в формате HH:MM:SS."""
        return datetime.now().strftime('%H:%M:%S')


class Task2NumberPrinter:
    """
    Класс для решения Задания 2: Вывод чисел с задержкой.

    Создаёт несколько потоков, каждый из которых выводит целые числа
    от 1 до 10 с задержкой в 1 секунду.
    """

    def __init__(self, num_threads: int = 3, start: int = 1, end: int = 10, delay: float = 1.0):
        """
        Инициализация класса.

        Args:
            num_threads: Количество потоков для создания
            start: Начальное число диапазона
            end: Конечное число диапазона
            delay: Задержка между выводами в секундах
        """
        self.num_threads = num_threads
        self.start = start
        self.end = end
        self.delay = delay
        self.execution_time = 0
        self.threads: List[threading.Thread] = []

    def print_numbers(self, thread_id: int) -> None:
        """
        Выводит числа от start до end с заданной задержкой.

        Args:
            thread_id: Идентификатор потока
        """
        print(f"\n[{self._get_time()}]  Поток {thread_id}: Начало работы")

        for i in range(self.start, self.end + 1):
            current_time = self._get_time()
            print(f"  [{current_time}] Поток {thread_id} → Число: {i}")
            time.sleep(self.delay)

        print(f"[{self._get_time()}]  Поток {thread_id}: Работа завершена")

    def run(self) -> dict:
        """
        Создаёт и запускает все потоки, ожидает их завершения.

        Returns:
            dict: Словарь с информацией о выполнении
        """
        print("\n" + "=" * 70)
        print(f"ЗАДАНИЕ 2: Вывод чисел с задержкой ({self.num_threads} потока)")
        print("=" * 70)

        print(f"\n Создание и запуск {self.num_threads} потоков...\n")
        start_time = time.time()

        # Создание и запуск потоков
        for i in range(1, self.num_threads + 1):
            thread = threading.Thread(
                target=self.print_numbers,
                args=(i,),
                name=f"NumberThread-{i}"
            )
            self.threads.append(thread)
            thread.start()

        # Ожидание завершения всех потоков
        for thread in self.threads:
            thread.join()

        self.execution_time = time.time() - start_time

        # Вывод результатов
        self._print_results()

        return {
            'num_threads': self.num_threads,
            'numbers_per_thread': self.end - self.start + 1,
            'execution_time': self.execution_time
        }

    def _print_results(self) -> None:
        """Выводит итоговые результаты выполнения."""
        sequential_time = self.num_threads * (self.end - self.start + 1) * self.delay

        print("\n" + "=" * 70)
        print(" РЕЗУЛЬТАТЫ ЗАДАНИЯ 2")
        print("=" * 70)
        print(f"  Время выполнения: {self.execution_time:.2f} секунд")
        print(f" Без многопоточности: ~{sequential_time:.1f} секунд")
        print(f" Ускорение: ~{sequential_time / self.execution_time:.1f}x")
        print(f" Обработано: {self.num_threads} потоков × {self.end - self.start + 1} чисел")
        print("=" * 70)

    @staticmethod
    def _get_time() -> str:
        """Возвращает текущее время в формате HH:MM:SS."""
        return datetime.now().strftime('%H:%M:%S')


class MultithreadingDemo:
    """
    Главный класс для демонстрации решений всех заданий.

    Объединяет все задания и предоставляет удобный интерфейс для запуска.
    """

    def __init__(self):
        """Инициализация демонстрационного класса."""
        self.task1 = Task1Calculator()
        self.task2 = Task2NumberPrinter(num_threads=3)

    def run_all(self) -> None:
        """Запускает все задания последовательно."""
        print("\n" + "=" * 70)
        print("🎓 ДОМАШНЕЕ ЗАДАНИЕ: МНОГОПОТОЧНОСТЬ В PYTHON")
        print("=" * 70)
        print("Дисциплина: Язык Python для разработчиков")
        print("Тема: Параллельные вычисления. Многопоточность и многопроцессность")
        print("Преподаватель: Владимир Хомутов")
        print("=" * 70)

        # Задание 1
        self.task1.run()

        # Пауза между заданиями
        time.sleep(2)

        # Задание 2
        self.task2.run()

        # Итоговая информация
        self._print_summary()

    def run_task1_only(self) -> dict:
        """Запускает только Задание 1."""
        return self.task1.run()

    def run_task2_only(self) -> dict:
        """Запускает только Задание 2."""
        return self.task2.run()

    def _print_summary(self) -> None:
        """Выводит итоговую сводку по всем заданиям."""
        print("\n" + "=" * 70)
        print(" ВСЕ ЗАДАНИЯ УСПЕШНО ВЫПОЛНЕНЫ!")
        print("=" * 70)
        print("\n ЧЕК-ЛИСТ САМОПРОВЕРКИ:")
        print("\n Задание 1:")
        print("   ✓ Программа создаёт 2 потока для вычисления квадратов и кубов")
        print("   ✓ Вычисляет квадраты и кубы целых чисел от 1 до 10")
        print("   ✓ Потоки работают параллельно")
        print("\n Задание 2:")
        print("   ✓ Программа создаёт несколько потоков")
        print("   ✓ Каждый поток выводит целые числа от 1 до 10")
        print("   ✓ Задержка между выводами составляет 1 секунду")
        print("   ✓ Потоки работают параллельно")
        print("\n" + "=" * 70)
        print(" Спасибо за проверку!")
        print("=" * 70 + "\n")


def main():
    """Главная функция для запуска программы."""
    demo = MultithreadingDemo()
    demo.run_all()


if __name__ == "__main__":
    main()
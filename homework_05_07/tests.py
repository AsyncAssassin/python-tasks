"""
Unit-тесты для модуля multithreading_homework.

Проверяет корректность работы всех классов и методов.
"""

import unittest
import time
import threading
import sys
import os

# Добавляем текущую директорию в путь поиска модулей
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from multithreading_homework import (
    Task1Calculator,
    Task2NumberPrinter,
    MultithreadingDemo
)


class TestTask1Calculator(unittest.TestCase):
    """Тесты для класса Task1Calculator."""

    def test_initialization(self):
        """Тест инициализации класса."""
        calculator = Task1Calculator(start=1, end=5)
        self.assertEqual(calculator.start, 1)
        self.assertEqual(calculator.end, 5)
        self.assertEqual(calculator.squares_results, [])
        self.assertEqual(calculator.cubes_results, [])

    def test_calculate_squares(self):
        """Тест вычисления квадратов."""
        calculator = Task1Calculator(start=1, end=5)
        calculator.calculate_squares()

        expected = [(1, 1), (2, 4), (3, 9), (4, 16), (5, 25)]
        self.assertEqual(calculator.squares_results, expected)

    def test_calculate_cubes(self):
        """Тест вычисления кубов."""
        calculator = Task1Calculator(start=1, end=5)
        calculator.calculate_cubes()

        expected = [(1, 1), (2, 8), (3, 27), (4, 64), (5, 125)]
        self.assertEqual(calculator.cubes_results, expected)

    def test_run_returns_correct_structure(self):
        """Тест структуры возвращаемых данных метода run."""
        calculator = Task1Calculator(start=1, end=3)
        results = calculator.run()

        self.assertIn('squares', results)
        self.assertIn('cubes', results)
        self.assertIn('execution_time', results)
        self.assertIsInstance(results['squares'], list)
        self.assertIsInstance(results['cubes'], list)
        self.assertIsInstance(results['execution_time'], float)

    def test_parallel_execution_time(self):
        """Тест, что параллельное выполнение быстрее последовательного."""
        calculator = Task1Calculator(start=1, end=5)

        # Параллельное выполнение
        results = calculator.run()
        parallel_time = results['execution_time']

        # Ожидаемое последовательное время (5 чисел * 0.1 сек * 2 операции)
        expected_sequential_time = 5 * 0.1 * 2

        # Параллельное должно быть быстрее
        self.assertLess(parallel_time, expected_sequential_time)

    def test_correct_results_length(self):
        """Тест корректности количества результатов."""
        calculator = Task1Calculator(start=1, end=10)
        results = calculator.run()

        self.assertEqual(len(results['squares']), 10)
        self.assertEqual(len(results['cubes']), 10)

    def test_custom_range(self):
        """Тест работы с пользовательским диапазоном."""
        calculator = Task1Calculator(start=5, end=8)
        results = calculator.run()

        self.assertEqual(len(results['squares']), 4)
        self.assertEqual(results['squares'][0], (5, 25))
        self.assertEqual(results['squares'][-1], (8, 64))


class TestTask2NumberPrinter(unittest.TestCase):
    """Тесты для класса Task2NumberPrinter."""

    def test_initialization(self):
        """Тест инициализации класса."""
        printer = Task2NumberPrinter(num_threads=3, start=1, end=10, delay=0.5)
        self.assertEqual(printer.num_threads, 3)
        self.assertEqual(printer.start, 1)
        self.assertEqual(printer.end, 10)
        self.assertEqual(printer.delay, 0.5)

    def test_default_parameters(self):
        """Тест параметров по умолчанию."""
        printer = Task2NumberPrinter()
        self.assertEqual(printer.num_threads, 3)
        self.assertEqual(printer.start, 1)
        self.assertEqual(printer.end, 10)
        self.assertEqual(printer.delay, 1.0)

    def test_run_returns_correct_structure(self):
        """Тест структуры возвращаемых данных."""
        printer = Task2NumberPrinter(num_threads=2, start=1, end=3, delay=0.1)
        results = printer.run()

        self.assertIn('num_threads', results)
        self.assertIn('numbers_per_thread', results)
        self.assertIn('execution_time', results)
        self.assertEqual(results['num_threads'], 2)
        self.assertEqual(results['numbers_per_thread'], 3)

    def test_execution_time_scaling(self):
        """Тест, что время выполнения примерно соответствует ожидаемому."""
        # 2 потока, 3 числа, задержка 0.1 сек
        printer = Task2NumberPrinter(num_threads=2, start=1, end=3, delay=0.1)
        results = printer.run()

        # Ожидаемое время: 3 числа * 0.1 сек = ~0.3 сек
        expected_time = 3 * 0.1

        # Проверяем с допуском ±0.2 сек
        self.assertAlmostEqual(results['execution_time'], expected_time, delta=0.2)

    def test_multiple_threads_created(self):
        """Тест создания нескольких потоков."""
        printer = Task2NumberPrinter(num_threads=5, delay=0.01)
        results = printer.run()

        self.assertEqual(len(printer.threads), 5)
        self.assertEqual(results['num_threads'], 5)

    def test_parallel_speedup(self):
        """Тест ускорения при параллельном выполнении."""
        num_threads = 3
        num_numbers = 5
        delay = 0.1

        printer = Task2NumberPrinter(
            num_threads=num_threads,
            start=1,
            end=num_numbers,
            delay=delay
        )
        results = printer.run()

        # Время параллельного выполнения
        parallel_time = results['execution_time']

        # Ожидаемое последовательное время
        sequential_time = num_threads * num_numbers * delay

        # Параллельное должно быть значительно быстрее
        self.assertLess(parallel_time, sequential_time * 0.5)


class TestMultithreadingDemo(unittest.TestCase):
    """Тесты для класса MultithreadingDemo."""

    def test_initialization(self):
        """Тест инициализации класса."""
        demo = MultithreadingDemo()
        self.assertIsInstance(demo.task1, Task1Calculator)
        self.assertIsInstance(demo.task2, Task2NumberPrinter)

    def test_run_task1_only(self):
        """Тест запуска только Задания 1."""
        demo = MultithreadingDemo()
        results = demo.run_task1_only()

        self.assertIn('squares', results)
        self.assertIn('cubes', results)
        self.assertIn('execution_time', results)

    def test_run_task2_only(self):
        """Тест запуска только Задания 2."""
        # Используем малые параметры для быстрого теста
        demo = MultithreadingDemo()
        demo.task2 = Task2NumberPrinter(num_threads=2, start=1, end=2, delay=0.1)

        results = demo.run_task2_only()

        self.assertIn('num_threads', results)
        self.assertIn('execution_time', results)

    def test_attributes_exist(self):
        """Тест наличия необходимых атрибутов."""
        demo = MultithreadingDemo()

        self.assertTrue(hasattr(demo, 'task1'))
        self.assertTrue(hasattr(demo, 'task2'))
        self.assertTrue(hasattr(demo, 'run_all'))
        self.assertTrue(hasattr(demo, 'run_task1_only'))
        self.assertTrue(hasattr(demo, 'run_task2_only'))


class TestThreadingBehavior(unittest.TestCase):
    """Дополнительные тесты поведения многопоточности."""

    def test_threads_run_concurrently(self):
        """Тест, что потоки действительно выполняются параллельно."""
        shared_data = {'thread1_time': None, 'thread2_time': None}

        def task1():
            time.sleep(0.1)
            shared_data['thread1_time'] = time.time()

        def task2():
            time.sleep(0.1)
            shared_data['thread2_time'] = time.time()

        t1 = threading.Thread(target=task1)
        t2 = threading.Thread(target=task2)

        start = time.time()
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        total_time = time.time() - start

        # Если потоки выполнялись параллельно, общее время ~0.1 сек, а не ~0.2 сек
        self.assertLess(total_time, 0.15)

        # Оба потока должны завершиться примерно в одно время
        time_diff = abs(shared_data['thread1_time'] - shared_data['thread2_time'])
        self.assertLess(time_diff, 0.05)


def run_tests():
    """Функция для запуска всех тестов."""
    # Создаём test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Добавляем все тестовые классы
    suite.addTests(loader.loadTestsFromTestCase(TestTask1Calculator))
    suite.addTests(loader.loadTestsFromTestCase(TestTask2NumberPrinter))
    suite.addTests(loader.loadTestsFromTestCase(TestMultithreadingDemo))
    suite.addTests(loader.loadTestsFromTestCase(TestThreadingBehavior))

    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Выводим итоги
    print("\n" + "=" * 70)
    print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("=" * 70)
    print(f"Пройдено тестов: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Провалено тестов: {len(result.failures)}")
    print(f"Ошибок: {len(result.errors)}")
    print("=" * 70)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
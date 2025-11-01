"""
Примеры использования классов для решения домашнего задания.

Этот файл демонстрирует различные способы использования классов
Task1Calculator и Task2NumberPrinter.
"""

from multithreading_homework import (
    Task1Calculator,
    Task2NumberPrinter,
    MultithreadingDemo
)


def example_1_basic_usage():
    """Пример 1: Базовое использование - запуск всех заданий."""
    print("\n" + "=" * 70)
    print("ПРИМЕР 1: Базовое использование")
    print("=" * 70)

    demo = MultithreadingDemo()
    demo.run_all()


def example_2_task1_only():
    """Пример 2: Запуск только Задания 1."""
    print("\n" + "=" * 70)
    print("ПРИМЕР 2: Только Задание 1")
    print("=" * 70)

    calculator = Task1Calculator()
    results = calculator.run()

    print("\nПолучены результаты:")
    print(f"Квадраты: {results['squares'][:3]}...")
    print(f"Кубы: {results['cubes'][:3]}...")
    print(f"Время: {results['execution_time']:.2f} сек")


def example_3_task1_custom_range():
    """Пример 3: Задание 1 с пользовательским диапазоном."""
    print("\n" + "=" * 70)
    print("ПРИМЕР 3: Задание 1 с диапазоном 1-5")
    print("=" * 70)

    calculator = Task1Calculator(start=1, end=5)
    results = calculator.run()

    print("\nПолные результаты:")
    print(f"Квадраты: {results['squares']}")
    print(f"Кубы: {results['cubes']}")


def example_4_task2_only():
    """Пример 4: Запуск только Задания 2."""
    print("\n" + "=" * 70)
    print("ПРИМЕР 4: Только Задание 2")
    print("=" * 70)

    printer = Task2NumberPrinter(num_threads=3)
    results = printer.run()

    print(f"\nСоздано потоков: {results['num_threads']}")
    print(f"Чисел на поток: {results['numbers_per_thread']}")


def example_5_task2_many_threads():
    """Пример 5: Задание 2 с большим количеством потоков."""
    print("\n" + "=" * 70)
    print("ПРИМЕР 5: Задание 2 с 5 потоками")
    print("=" * 70)

    printer = Task2NumberPrinter(num_threads=5)
    printer.run()


def example_6_task2_custom_parameters():
    """Пример 6: Задание 2 с пользовательскими параметрами."""
    print("\n" + "=" * 70)
    print("ПРИМЕР 6: Пользовательские параметры")
    print("=" * 70)
    print("2 потока, числа 1-5, задержка 0.5 сек\n")

    printer = Task2NumberPrinter(
        num_threads=2,
        start=1,
        end=5,
        delay=0.5
    )
    printer.run()


def example_7_both_tasks_separately():
    """Пример 7: Запуск заданий по отдельности через главный класс."""
    print("\n" + "=" * 70)
    print("ПРИМЕР 7: Отдельный запуск через MultithreadingDemo")
    print("=" * 70)

    demo = MultithreadingDemo()

    print("\nЗапускаем Задание 1...")
    demo.run_task1_only()

    print("\nПауза 2 секунды...\n")
    import time
    time.sleep(2)

    print("Запускаем Задание 2...")
    demo.run_task2_only()


def main():
    """Главная функция с меню выбора примера."""
    examples = {
        '1': ('Базовое использование (все задания)', example_1_basic_usage),
        '2': ('Только Задание 1', example_2_task1_only),
        '3': ('Задание 1 с диапазоном 1-5', example_3_task1_custom_range),
        '4': ('Только Задание 2', example_4_task2_only),
        '5': ('Задание 2 с 5 потоками', example_5_task2_many_threads),
        '6': ('Задание 2 с кастомными параметрами', example_6_task2_custom_parameters),
        '7': ('Оба задания отдельно', example_7_both_tasks_separately),
        '0': ('Запустить все примеры подряд', None)
    }

    print("\n" + "=" * 70)
    print("ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ")
    print("=" * 70)
    print("\nВыберите пример для запуска:\n")

    for key, (description, _) in examples.items():
        print(f"  {key}. {description}")

    print("\n" + "=" * 70)
    choice = input("\nВведите номер примера (или Enter для примера 1): ").strip()

    if not choice:
        choice = '1'

    if choice == '0':
        # Запустить все примеры
        for key in sorted(examples.keys()):
            if key != '0' and examples[key][1]:
                examples[key][1]()
                print("\n" + "=" * 70)
                print("Пауза 3 секунды перед следующим примером...")
                print("=" * 70)
                import time
                time.sleep(3)
    elif choice in examples and examples[choice][1]:
        examples[choice][1]()
    else:
        print("Неверный выбор. Запускаем пример 1...\n")
        example_1_basic_usage()


if __name__ == "__main__":
    main()
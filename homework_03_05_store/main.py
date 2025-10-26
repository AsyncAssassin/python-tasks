#main.py
# Основной пример использования из задания
from product import Product
from order import Order
from store import Store
if __name__ == "__main__":
    print("=" * 60)
    print("ОСНОВНОЕ ЗАДАНИЕ - Пример использования")
    print("=" * 60 + "\n")

    # Создаем магазин
    store = Store()

    # Создаем товары
    product1 = Product("Ноутбук", 1000, 5)
    product2 = Product("Смартфон", 500, 10)

    # Добавляем товары в магазин
    store.add_product(product1)
    store.add_product(product2)

    # Список всех товаров
    store.list_products()

    # Создаем заказ
    order = store.create_order()

    # Добавляем товары в заказ
    order.add_product(product1, 2)
    order.add_product(product2, 3)

    # Выводим общую стоимость заказа
    total = order.calculate_total()
    print(f"\nОбщая стоимость заказа: {total} руб.\n")

    # Проверяем остатки на складе после заказа
    store.list_products()

    print("\n" + "=" * 60)
    print("ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ 1 - Удаление товаров из заказа")
    print("=" * 60 + "\n")

    # Создаём новый заказ для демонстрации
    order2 = store.create_order()
    order2.add_product(product1, 1)
    order2.add_product(product2, 2)

    print(f"\n{order2}\n")

    # Удаляем товар из заказа
    order2.remove_product(product2, 1)

    print(f"\n{order2}\n")

    store.list_products()

    print("\n" + "=" * 60)
    print("ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ 2 - Возврат товаров")
    print("=" * 60 + "\n")

    # Создаём новый товар
    product3 = Product("Наушники", 100, 20)
    store.add_product(product3)

    # Создаём заказ
    order3 = store.create_order()
    order3.add_product(product3, 5)

    print(f"\n{order3}\n")

    store.list_products()

    # Возвращаем часть товара
    order3.return_product(product3, 3)

    print(f"\n{order3}\n")

    store.list_products()

    print("\n" + "=" * 60)
    print("ПРОВЕРКА ОБРАБОТКИ ОШИБОК")
    print("=" * 60 + "\n")

    # Пытаемся заказать больше, чем есть на складе
    print("1. Попытка заказать больше, чем есть на складе:")
    order4 = store.create_order()
    order4.add_product(product1, 10)  # На складе только 2 ноутбука

    print("\n2. Попытка удалить товар, которого нет в заказе:")
    order4.remove_product(product3, 1)

    print("\n3. Попытка вернуть больше, чем есть в заказе:")
    order3.return_product(product3, 10)

    print("\n" + "=" * 60)
    print("ЗАДАНИЕ ВЫПОЛНЕНО!")
    print("=" * 60)

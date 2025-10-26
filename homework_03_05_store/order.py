#order.py
from product import Product
class Order:
    """
    Класс для представления заказа.

    Атрибуты:
        products (dict): Словарь {Product: количество}
    """

    def __init__(self):
        """Инициализация пустого заказа."""
        self.products = {}

    def add_product(self, product, quantity):
        """
        Добавляет товар в заказ.

        Args:
            product (Product): Товар для добавления
            quantity (int): Количество товара

        Returns:
            bool: True если добавление успешно, False если ошибка
        """
        if quantity <= 0:
            print(f"Ошибка: Количество должно быть положительным числом.")
            return False

        # Проверяем доступность товара на складе
        if product.stock < quantity:
            print(f"Ошибка: Недостаточно товара '{product.name}' на складе. "
                  f"Доступно: {product.stock} шт., запрошено: {quantity} шт.")
            return False

        # Обновляем количество товара на складе
        product.update_stock(-quantity)

        # Добавляем товар в заказ
        if product in self.products:
            self.products[product] += quantity
        else:
            self.products[product] = quantity

        print(f"Товар '{product.name}' ({quantity} шт.) добавлен в заказ.")
        return True

    def calculate_total(self):
        """
        Рассчитывает общую стоимость заказа.

        Returns:
            float: Общая стоимость заказа
        """
        total = sum(product.price * quantity
                    for product, quantity in self.products.items())
        return total

    def remove_product(self, product, quantity):
        """
        Удаляет товар из заказа (дополнительное задание 1).

        Args:
            product (Product): Товар для удаления
            quantity (int): Количество товара для удаления

        Returns:
            bool: True если удаление успешно, False если ошибка
        """
        if product not in self.products:
            print(f"Ошибка: Товар '{product.name}' отсутствует в заказе.")
            return False

        if quantity <= 0:
            print(f"Ошибка: Количество должно быть положительным числом.")
            return False

        current_quantity = self.products[product]

        if quantity > current_quantity:
            print(f"Ошибка: В заказе только {current_quantity} шт. товара '{product.name}', "
                  f"нельзя удалить {quantity} шт.")
            return False

        # Возвращаем товар на склад
        product.update_stock(quantity)

        # Обновляем количество в заказе
        self.products[product] -= quantity

        # Если количество стало 0, удаляем товар из заказа
        if self.products[product] == 0:
            del self.products[product]
            print(f"Товар '{product.name}' ({quantity} шт.) полностью удалён из заказа.")
        else:
            print(f"Товар '{product.name}' ({quantity} шт.) удалён из заказа. "
                  f"Осталось в заказе: {self.products[product]} шт.")

        return True

    def return_product(self, product, quantity):
        """
        Возвращает товар из заказа обратно в магазин (дополнительное задание 2).

        Args:
            product (Product): Товар для возврата
            quantity (int): Количество товара для возврата

        Returns:
            bool: True если возврат успешен, False если ошибка
        """
        if product not in self.products:
            print(f"Ошибка: Товар '{product.name}' отсутствует в заказе.")
            return False

        if quantity <= 0:
            print(f"Ошибка: Количество должно быть положительным числом.")
            return False

        current_quantity = self.products[product]

        if quantity > current_quantity:
            print(f"Ошибка: В заказе только {current_quantity} шт. товара '{product.name}', "
                  f"нельзя вернуть {quantity} шт.")
            return False

        # Возвращаем товар на склад
        product.update_stock(quantity)

        # Уменьшаем количество в заказе
        self.products[product] -= quantity

        # Если количество стало 0, удаляем товар из заказа
        if self.products[product] == 0:
            del self.products[product]
            print(f"Товар '{product.name}' ({quantity} шт.) возвращён на склад и удалён из заказа.")
        else:
            print(f"Товар '{product.name}' ({quantity} шт.) возвращён на склад. "
                  f"Осталось в заказе: {self.products[product]} шт.")

        return True

    def __str__(self):
        """Строковое представление заказа."""
        if not self.products:
            return "Заказ пуст"

        order_str = "Заказ содержит:\n"
        for product, quantity in self.products.items():
            order_str += f"  - {product.name}: {quantity} шт. x {product.price} руб. = {quantity * product.price} руб.\n"
        order_str += f"Итого: {self.calculate_total()} руб."
        return order_str

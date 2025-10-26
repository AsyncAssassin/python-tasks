#product.py
class Product:
    """
    Класс для представления товара в магазине.

    Атрибуты:
        name (str): Название товара
        price (float): Цена товара
        stock (int): Количество товара на складе
    """

    def __init__(self, name, price, stock):
        """
        Инициализация товара.

        Args:
            name (str): Название товара
            price (float): Цена товара
            stock (int): Начальное количество на складе
        """
        self.name = name
        self.price = price
        self.stock = stock

    def update_stock(self, quantity):
        """
        Обновляет количество товара на складе.

        Args:
            quantity (int): Изменение количества (может быть отрицательным)

        Returns:
            bool: True если обновление успешно, False если ошибка
        """
        new_stock = self.stock + quantity

        if new_stock < 0:
            print(f"Ошибка: Недостаточно товара '{self.name}' на складе. "
                  f"Доступно: {self.stock}, запрошено: {abs(quantity)}")
            return False

        self.stock = new_stock
        return True

    def __str__(self):
        """Строковое представление товара."""
        return f"{self.name} - {self.price} руб. (В наличии: {self.stock} шт.)"


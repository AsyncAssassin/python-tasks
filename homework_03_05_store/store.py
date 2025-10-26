#store.py
from order import Order
class Store:
    """
    Класс для представления магазина.

    Атрибуты:
        products (list): Список всех доступных товаров
    """

    def __init__(self):
        """Инициализация магазина с пустым списком товаров."""
        self.products = []

    def add_product(self, product):
        """
        Добавляет товар в магазин.

        Args:
            product (Product): Товар для добавления
        """
        self.products.append(product)
        print(f"Товар '{product.name}' добавлен в магазин.")

    def list_products(self):
        """Отображает все товары в магазине с их ценами и количеством на складе."""
        if not self.products:
            print("Магазин пуст.")
            return

        print("\n" + "=" * 60)
        print("Список товаров в магазине:")
        print("=" * 60)
        for i, product in enumerate(self.products, 1):
            print(f"{i}. {product}")
        print("=" * 60 + "\n")

    def create_order(self):
        """
        Создаёт новый заказ.

        Returns:
            Order: Новый объект заказа
        """
        print("Создан новый заказ.")
        return Order()
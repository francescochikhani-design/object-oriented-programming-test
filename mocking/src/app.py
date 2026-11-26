from dataclasses import dataclass


def calculate_discount(price, discount_percent):
    if price < 0:
        raise ValueError("Price must be nonnegative")
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100")
    return round(price - price * discount_percent / 100, 2)


def calculate_tax(price, tax_rate=0.20):
    return round(price * tax_rate, 2)


def calculate_total(prices, tax_rate=0.20):
    subtotal = sum(prices)
    return round(subtotal + calculate_tax(subtotal, tax_rate), 2)


@dataclass(frozen=True)
class Product:
    name: str
    price: float
    stock: int


class ProductRepository:
    def __init__(self):
        self._products = {
            "SHIRT": Product("T-Shirt", 25, 50),
            "MUG": Product("Coffee Mug", 12, 100),
            "HAT": Product("Cap", 18, 30),
        }

    def get_product(self, sku):
        return self._products.get(sku)

    def update_stock(self, sku, quantity):
        product = self.get_product(sku)
        if product is None or not 0 < quantity <= product.stock:
            return False
        self._products[sku] = Product(product.name, product.price, product.stock - quantity)
        return True


class OrderService:
    def __init__(self, repository):
        self.repository = repository

    def place_order(self, sku, quantity):
        product = self.repository.get_product(sku)
        if product is None:
            return {"success": False, "error": "Product not found"}
        if type(quantity) is not int or quantity <= 0:
            return {"success": False, "error": "Quantity must be a positive integer"}
        if not self.repository.update_stock(sku, quantity):
            return {"success": False, "error": "Not enough stock"}
        return {"success": True, "item": product.name, "quantity": quantity,
                "total": calculate_total([product.price * quantity])}

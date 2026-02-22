import json
import csv
from datetime import datetime
from typing import Dict, Any, Iterator, Optional


# -------------------- Exceptions --------------------
class InventoryError(Exception):
    pass

class ProductNotFoundError(InventoryError):
    pass

class DuplicateProductError(InventoryError):
    pass

class InvalidDataError(InventoryError):
    pass

# -------------------- Decorator (Logging) --------------------
def log_action(action_name: str):
    """
    Decorator to log inventory actions to a file with timestamp.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            try:
                with open("inventory.log", "a", encoding="utf-8") as f:
                    f.write(f"[{datetime.now().isoformat(timespec='seconds')}] {action_name}\n")
            except Exception:
                # Logging should never crash the app
                pass
            return result
        return wrapper
    return decorator


# -------------------- Product Classes (OOP: Encapsulation + Inheritance + Polymorphism) --------------------
class Product:
    def __init__(self, product_id: str, name: str, price: float, stock: int):
        self.__product_id = product_id.strip()
        self.__name = name.strip()
        self.__price = price
        self.__stock = stock
        self._validate()

    # ---- Encapsulation: getters/setters ----
    @property
    def product_id(self) -> str:
        return self.__product_id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        value = value.strip()
        if not value:
            raise InvalidDataError("Name cannot be empty.")
        self.__name = value

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value: float) -> None:
        try:
            value = float(value)
        except Exception:
            raise InvalidDataError("Price must be a number.")
        if value < 0:
            raise InvalidDataError("Price cannot be negative.")
        self.__price = value

    @property
    def stock(self) -> int:
        return self.__stock

    @stock.setter
    def stock(self, value: int) -> None:
        try:
            value = int(value)
        except Exception:
            raise InvalidDataError("Stock must be an integer.")
        if value < 0:
            raise InvalidDataError("Stock cannot be negative.")
        self.__stock = value

    def _validate(self) -> None:
        if not self.__product_id:
            raise InvalidDataError("Product ID cannot be empty.")
        if not self.__name:
            raise InvalidDataError("Product name cannot be empty.")
        if not isinstance(self.__price, (int, float)) or self.__price < 0:
            raise InvalidDataError("Invalid price.")
        if not isinstance(self.__stock, int) or self.__stock < 0:
            raise InvalidDataError("Invalid stock.")

    # ---- Polymorphism: subclasses can extend these ----
    def category(self) -> str:
        return "Product"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.__class__.__name__,
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Product":
        ptype = data.get("type")
        if ptype == "Electronics":
            return Electronics(
                data["product_id"], data["name"], data["price"], data["stock"],
                brand=data.get("brand", ""), warranty_months=data.get("warranty_months", 0)
            )
        if ptype == "Grocery":
            return Grocery(
                data["product_id"], data["name"], data["price"], data["stock"],
                expiry_date=data.get("expiry_date", "")
            )
        # fallback
        return Product(data["product_id"], data["name"], data["price"], data["stock"])

    def __str__(self) -> str:
        return f"{self.category():<12} | ID: {self.product_id:<10} | {self.name:<20} | ₹{self.price:<8.2f} | Stock: {self.stock}"


class Electronics(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, brand: str, warranty_months: int):
        self.__brand = brand.strip()
        self.__warranty_months = int(warranty_months) if str(warranty_months).strip() else 0
        super().__init__(product_id, name, price, stock)

    @property
    def brand(self) -> str:
        return self.__brand

    @brand.setter
    def brand(self, value: str) -> None:
        self.__brand = value.strip()

    @property
    def warranty_months(self) -> int:
        return self.__warranty_months

    @warranty_months.setter
    def warranty_months(self, value: int) -> None:
        try:
            value = int(value)
        except Exception:
            raise InvalidDataError("Warranty must be an integer (months).")
        if value < 0:
            raise InvalidDataError("Warranty cannot be negative.")
        self.__warranty_months = value

    def category(self) -> str:
        return "Electronics"

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({"brand": self.brand, "warranty_months": self.warranty_months})
        return d

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base} | Brand: {self.brand:<10} | Warranty: {self.warranty_months}m"


class Grocery(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, expiry_date: str):
        self.__expiry_date = expiry_date.strip()  # keep simple: string like "2026-12-31"
        super().__init__(product_id, name, price, stock)

    @property
    def expiry_date(self) -> str:
        return self.__expiry_date

    @expiry_date.setter
    def expiry_date(self, value: str) -> None:
        self.__expiry_date = value.strip()

    def category(self) -> str:
        return "Grocery"

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({"expiry_date": self.expiry_date})
        return d

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base} | Exp: {self.expiry_date or 'N/A'}"


# -------------------- Custom Iterator --------------------
class InventoryIterator:
    def __init__(self, products_list):
        self._products = products_list
        self._index = 0

    def __iter__(self) -> "InventoryIterator":
        return self

    def __next__(self) -> Product:
        if self._index >= len(self._products):
            raise StopIteration
        item = self._products[self._index]
        self._index += 1
        return item


# -------------------- Inventory (Manages Products) --------------------
class Inventory:
    def __init__(self):
        self.__products: Dict[str, Product] = {}  # private

    # Custom iterator support
    def __iter__(self) -> Iterator[Product]:
        return InventoryIterator(list(self.__products.values()))

    def _exists(self, product_id: str) -> bool:
        return product_id in self.__products

    @log_action("ADD_PRODUCT")
    def add_product(self, product: Product) -> None:
        if self._exists(product.product_id):
            raise DuplicateProductError(f"Product with ID '{product.product_id}' already exists.")
        self.__products[product.product_id] = product

    @log_action("REMOVE_PRODUCT")
    def remove_product(self, product_id: str) -> None:
        product_id = product_id.strip()
        if not self._exists(product_id):
            raise ProductNotFoundError(f"No product found with ID '{product_id}'.")
        del self.__products[product_id]

    @log_action("UPDATE_STOCK")
    def update_stock(self, product_id: str, new_stock: int) -> None:
        product_id = product_id.strip()
        if not self._exists(product_id):
            raise ProductNotFoundError(f"No product found with ID '{product_id}'.")
        self.__products[product_id].stock = new_stock

    @log_action("UPDATE_PRICE")
    def update_price(self, product_id: str, new_price: float) -> None:
        product_id = product_id.strip()
        if not self._exists(product_id):
            raise ProductNotFoundError(f"No product found with ID '{product_id}'.")
        self.__products[product_id].price = new_price

    def get_product(self, product_id: str) -> Product:
        product_id = product_id.strip()
        if not self._exists(product_id):
            raise ProductNotFoundError(f"No product found with ID '{product_id}'.")
        return self.__products[product_id]

    def search(self, keyword: str) -> list[Product]:
        keyword = keyword.strip().lower()
        if not keyword:
            return []
        results = []
        for p in self.__products.values():
            if keyword in p.product_id.lower() or keyword in p.name.lower() or keyword in p.category().lower():
                results.append(p)
        return results

    @log_action("SAVE_JSON")
    def save_to_json(self, filename: str) -> None:
        data = [p.to_dict() for p in self.__products.values()]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @log_action("LOAD_JSON")
    def load_from_json(self, filename: str) -> None:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise InvalidDataError("Invalid JSON format: expected a list.")
        loaded: Dict[str, Product] = {}
        for item in data:
            p = Product.from_dict(item)
            loaded[p.product_id] = p
        self.__products = loaded

    @log_action("EXPORT_CSV")
    def export_to_csv(self, filename: str) -> None:
        rows = [p.to_dict() for p in self.__products.values()]
        # Find all keys (because Electronics/Grocery have extra fields)
        all_keys = set()
        for r in rows:
            all_keys.update(r.keys())
        fieldnames = sorted(all_keys)

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def list_all(self) -> list[Product]:
        return list(self.__products.values())


# -------------------- Console UI --------------------
def read_int(prompt: str) -> int:
    value = input(prompt).strip()
    try:
        return int(value)
    except Exception:
        raise InvalidDataError("Please enter a valid integer.")


def read_float(prompt: str) -> float:
    value = input(prompt).strip()
    try:
        return float(value)
    except Exception:
        raise InvalidDataError("Please enter a valid number.")


def create_product_from_user() -> Product:
    print("\nChoose product type:")
    print("1) Electronics")
    print("2) Grocery")
    choice = input("Enter choice (1/2): ").strip()

    product_id = input("Product ID: ").strip()
    name = input("Name: ").strip()
    price = read_float("Price: ")
    stock = read_int("Stock: ")

    if choice == "1":
        brand = input("Brand: ").strip()
        warranty = read_int("Warranty (months): ")
        return Electronics(product_id, name, price, stock, brand, warranty)

    if choice == "2":
        expiry = input("Expiry date (YYYY-MM-DD) (optional): ").strip()
        return Grocery(product_id, name, price, stock, expiry)

    raise InvalidDataError("Invalid product type choice.")


def print_products(products: list[Product]) -> None:
    if not products:
        print("No products found.")
        return
    print("\n--- Products ---")
    for p in products:
        print(p)


def main():
    inv = Inventory()
    default_file = "inventory.json"

    while True:
        print("\n========== INVENTORY MENU ==========")
        print("1) Add product")
        print("2) Remove product")
        print("3) Update stock")
        print("4) Update price")
        print("5) Search product")
        print("6) List all products")
        print("7) Save to JSON")
        print("8) Load from JSON")
        print("9) Export to CSV")
        print("0) Exit")
        choice = input("Enter choice: ").strip()

        try:
            if choice == "1":
                product = create_product_from_user()
                inv.add_product(product)
                print("✅ Product added.")

            elif choice == "2":
                pid = input("Enter Product ID to remove: ").strip()
                inv.remove_product(pid)
                print("✅ Product removed.")

            elif choice == "3":
                pid = input("Enter Product ID to update stock: ").strip()
                new_stock = read_int("Enter new stock: ")
                inv.update_stock(pid, new_stock)
                print("✅ Stock updated.")

            elif choice == "4":
                pid = input("Enter Product ID to update price: ").strip()
                new_price = read_float("Enter new price: ")
                inv.update_price(pid, new_price)
                print("✅ Price updated.")

            elif choice == "5":
                keyword = input("Enter keyword (id/name/type): ").strip()
                results = inv.search(keyword)
                print_products(results)

            elif choice == "6":
                # Demonstrates custom iterator usage:
                print("\n--- All Products (Iterated) ---")
                any_found = False
                for p in inv:
                    any_found = True
                    print(p)
                if not any_found:
                    print("No products in inventory.")

            elif choice == "7":
                filename = input(f"Enter JSON filename (default {default_file}): ").strip() or default_file
                inv.save_to_json(filename)
                print(f"✅ Saved to {filename}")

            elif choice == "8":
                filename = input(f"Enter JSON filename (default {default_file}): ").strip() or default_file
                inv.load_from_json(filename)
                print(f"✅ Loaded from {filename}")

            elif choice == "9":
                filename = input("Enter CSV filename (default inventory.csv): ").strip() or "inventory.csv"
                inv.export_to_csv(filename)
                print(f"✅ Exported to {filename}")

            elif choice == "0":
                print("Bye 👋")
                break

            else:
                print("❌ Invalid choice. Try again.")

        except InventoryError as e:
            print(f"❌ Error: {e}")
        except FileNotFoundError:
            print("❌ File not found. Check filename and try again.")
        except json.JSONDecodeError:
            print("❌ Invalid JSON file content.")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()

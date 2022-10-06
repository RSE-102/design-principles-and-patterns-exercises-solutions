# TODO: This class does not scale well in case export to other file formats is to be added.
#       (Also, the current implementation violates the DRY principle).
#       To solve these issues, use dependency injection to make it possible to export a
#       shopping cart into new data formats without having to change the `ShoppingCart` at all.
#
#       Note: in case you were wondering, we ignore product prices here because price handling
#             may have been changed in exercise_1
from typing import Protocol
from dataclasses import dataclass
from datetime import datetime
from exercise_1 import Product


class ShoppingCartWriter(Protocol):
    def add_product_specs(self, *, name: str, **kwargs) -> None:
        """Insert a product, given its name and an arbitrary number of additional key-value pairs"""
        ...


class ShoppingCart:
    @dataclass
    class _Entry:
        quantity: int
        last_modified: str

    def __init__(self) -> None:
        self._products: dict = {}

    def add(self, product: Product) -> None:
        if product.name not in self._products:
            self._products[product.name] = self._make_new_entry()
        self._products[product.name].quantity += 1
        self._products[product.name].last_modified = self._get_timestamp()

    def export(self, writer: ShoppingCartWriter) -> None:
        for name, entry in self._products.items():
            writer.add_product_specs(
                name=name,
                quantity=entry.quantity,
                last_modified=entry.last_modified
            )

    def _make_new_entry(self) -> _Entry:
        return self._Entry(quantity=0, last_modified=self._get_timestamp())

    def _get_timestamp(self) -> str:
        return datetime.now().isoformat()


class XMLShoppingCartWriter:
    def __init__(self, filename: str) -> None:
        self._file = open(filename, "w")
        self._write_product_list_begin()

    def __del__(self) -> None:
        self._write_product_list_end()
        self._file.close()

    def add_product_specs(self, *, name: str, **kwargs) -> None:
        self._file.write(f"  <Product name=\"{name}\"")
        for key, value in kwargs.items():
            self._file.write(f" {key}=\"{value}\"")
        self._file.write("/>\n")

    def _write_product_list_begin(self) -> None:
        self._file.write("<Products>\n")

    def _write_product_list_end(self) -> None:
        self._file.write("</Products>\n")


class JSONShoppingCartWriter:
    def __init__(self, filename: str) -> None:
        self._file = open(filename, "w")
        self._empty = True
        self._write_product_list_begin()

    def __del__(self) -> None:
        self._write_product_list_end()
        self._file.close()

    def add_product_specs(self, *, name: str, **kwargs) -> None:
        self._file.write("," if not self._empty else "")
        self._file.write(f'{{"name":"{name}"')
        for key, value in kwargs.items():
            self._file.write(f',"{key}":"{value}"')
        self._file.write("}")
        self._empty = False

    def _write_product_list_begin(self) -> None:
        self._file.write('{"products":[')

    def _write_product_list_end(self) -> None:
        self._file.write("]}")


if __name__ == "__main__":
    xml_filename = "cart.xml"
    json_filename = "cart.json"

    cart = ShoppingCart()
    cart.add(Product("Laptop", "999.00"))
    cart.add(Product("Keyboard", "10.00"))
    cart.add(Product("Keyboard", "10.00"))
    cart.export(XMLShoppingCartWriter(xml_filename))
    cart.export(JSONShoppingCartWriter(json_filename))

    for filename in [xml_filename, json_filename]:
        print(f"Content of '{filename}':")
        print(open(filename).read())

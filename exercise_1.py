from __future__ import annotations
from decimal import Decimal


class Money:
    def __init__(self, amount: str) -> None:
        self._amount = Decimal(self._format_amount(amount))

    def __add__(self, other: Money) -> Money:
        return Money(str(self._amount + other._amount))

    def __sub__(self, other: Money) -> Money:
        return Money(str(self._amount - other._amount))

    def __mul__(self, value: float) -> Money:
        result = self._round_to_valid_amount(
            self._amount*Decimal(value)
        )
        return Money(str(result))

    def __truediv__(self, value: float) -> Money:
        result = self._round_to_valid_amount(
            self._amount/Decimal(value)
        )
        return Money(str(result))

    def __repr__(self) -> str:
        return str(self._amount)

    def _format_amount(self, money_str: str) -> str:
        if "." not in money_str:
            return f"{money_str}.00"
        elif len(money_str.split(".")[1]) != 2:
            raise IOError("Too many decimal digits")
        return money_str

    def _round_to_valid_amount(self, value: Decimal) -> Decimal:
        return value.quantize(Decimal("1.00"))


class Discount:
    def __init__(self, percentage: float) -> None:
        assert percentage >= 0.0 and percentage <= 100.0
        self._value = percentage/100.0

    def __mul__(self, price: Money) -> Money:
        return price*(float(self._value))


class Product:
    def __init__(self, name: str, price: Money) -> None:
        self._name = name
        self._price = price

    def __repr__(self) -> str:
        return f"Product: {self._name}, price: {self._price}"

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> Money:
        return self._price

    def reduced(self, discount: Discount) -> Product:
        assert not self._is_reduced()
        return Product(
            name=f"{self._name}{self._reduced_suffix()}",
            price=self._price - discount*self._price
        )

    def _is_reduced(self) -> bool:
        return self._reduced_suffix() in self._name

    def _reduced_suffix(self) -> str:
        return " (reduced)"


if __name__ == "__main__":
    print(Product("Laptop", Money("999.00")))
    print(Product("Laptop", Money("999.00")).reduced(Discount(30.0)))

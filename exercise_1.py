# This solutions pulls out the representation of amounts of money
# into a separate class. This `Money` class makes sure that it can
# only be constructed by a valid string representing money, i.e. we
# requires no or 2 digits after the comma. It implements the required
# interfaces to add/subtract amounts of money, and multiply/divide
# by a scalar value.
#
# Moreover, we have pulled out the handling of discounts into a separate
# class, which now allows to apply a discount on a given price, and this
# class now is the central place in which we define & check what a valid
# discount is (here: between 0 and 100 %)

from __future__ import annotations
from decimal import Decimal


class Money:
    def __init__(self, amount: str | Decimal) -> None:
        if isinstance(amount, str):
            self._amount = Decimal(self._format_amount(amount))
        else:
            assert amount.same_quantum(self._get_representative_decimal())
            self._amount = amount

    def __add__(self, other: Money) -> Money:
        return Money(self._amount + other._amount)

    def __sub__(self, other: Money) -> Money:
        return Money(self._amount - other._amount)

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
        return value.quantize(self._get_representative_decimal())

    def _get_representative_decimal(self) -> Decimal:
        return Decimal("1.00")


class Discount:
    def __init__(self, percentage: float) -> None:
        assert percentage >= 0.0 and percentage <= 100.0
        self._value = percentage/100.0

    def apply(self, price: Money) -> Money:
        return price*(1.0 - self._value)


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
            price=discount.apply(self._price)
        )

    def _is_reduced(self) -> bool:
        return self._reduced_suffix() in self._name

    def _reduced_suffix(self) -> str:
        return " (reduced)"


if __name__ == "__main__":
    print(Product("Laptop", Money("999.00")))
    print(Product("Laptop", Money("999.00")).reduced(Discount(30.0)))

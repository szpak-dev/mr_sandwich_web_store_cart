from dataclasses import dataclass


@dataclass(frozen=True)
class CartId:
    id: int


@dataclass(frozen=True)
class CartProductId:
    id: int


@dataclass(frozen=True)
class CustomerId:
    id: int

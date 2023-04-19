from dataclasses import dataclass


@dataclass(frozen=True)
class ProductId:
    id: int

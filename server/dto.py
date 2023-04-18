from dataclasses import dataclass
from collections import namedtuple


@dataclass
class Item:
    name: str
    price: int


Inventory = namedtuple('Inventory', 'item count')

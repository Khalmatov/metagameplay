import json
from dataclasses import dataclass, asdict


@dataclass
class Item:
    name: str
    price: int


@dataclass
class UserItem(Item):
    count: int


@dataclass
class User:
    name: str
    balance: int
    items: list[UserItem]

    def as_json(self) -> str:
        _dict = asdict(self)
        return json.dumps(_dict, ensure_ascii=False)

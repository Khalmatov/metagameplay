import json
from dataclasses import dataclass, asdict


class BaseModel:
    def as_json(self) -> str:
        _dict = asdict(self)
        return json.dumps(_dict, ensure_ascii=False)


@dataclass
class Item(BaseModel):
    name: str
    price: int


@dataclass
class UserItem(Item):
    count: int


@dataclass
class User(BaseModel):
    name: str
    balance: int
    items: list[UserItem]

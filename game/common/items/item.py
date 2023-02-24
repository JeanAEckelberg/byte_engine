from game.common.enums import ObjectType
from game.common.game_object import GameObject
from typing import Self


class Item(GameObject):
    def __init__(self, value: int, durability: float = 1):
        super().__init__()
        self.object_type = ObjectType.ITEM
        self.value = value
        # durability starts as 1; treated as percent where 1 = 100%
        self.durability = durability
        
    @property
    def durability(self) -> float:
        return self.__durability

    @property
    def value(self) -> int:
        return self.__value

    @durability.setter
    def durability(self, durability: float):
        if not isinstance(durability, float):
            raise ValueError(f'Durability for {self.object_type.name} must be a float type.')
        self.__durability = min(max(durability, 0), 1)

    @value.setter
    def value(self, value: int):
        if not isinstance(value, int):
            raise ValueError(f'Value for {self.object_type.name} must be a int type.')
        self.__value = value

    def to_json(self):
        data = super().to_json()
        data['durability'] = self.durability
        data['value'] = self.value
        return data

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.durability = data['durability']
        self.value = data['value']
        return self

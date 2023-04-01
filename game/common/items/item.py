from game.common.enums import ObjectType
from game.common.game_object import GameObject
from typing import Self


class Item(GameObject):
    def __init__(self, value: int = 1, durability: int | None = 100, quantity: int = 1, stack_size: int = 0):
        super().__init__()
        self.object_type: ObjectType = ObjectType.ITEM
        self.value: int = value  # Value can more specified based on purpose (e.g., the sell price)
        self.durability: int | None = durability  # durability can be None if infinite durability
        self.quantity: int = quantity  # the current amount of this item
        self.stack_size = stack_size  # the max quantity this item can contain

    @property
    def durability(self) -> int | None:
        return self.__durability

    @property
    def value(self) -> int:
        return self.__value

    @property
    def quantity(self) -> int:
        return self.__quantity

    @property
    def stack_size(self) -> int:
        return self.__stack_size

    @durability.setter
    def durability(self, durability: int | None) -> int | None:
        if durability is not None and not isinstance(durability, int):
            raise ValueError(f'{self.__class__.__name__}.durability must be an int or None.')
        self.__durability = durability

    @value.setter
    def value(self, value: int) -> None:
        if value is None or not isinstance(value, int):
            raise ValueError(f'{self.__class__.__name__}.value must be an int.')
        self.__value = value

    @quantity.setter
    def quantity(self, quantity: int) -> int:

        if quantity is None or not isinstance(quantity, int):
            raise ValueError(f'{self.__class__.__name__}.quantity must be an int.')
        if quantity < 0:
            raise ValueError(f'{self.__class__.__name__}.quantity must be greater than 0.')
        self.__quantity = quantity

    @stack_size.setter
    def stack_size(self, stack_size: int) -> int:
        if stack_size is not isinstance(stack_size, int) or stack_size < self.quantity:
            raise ValueError(f'{self.__class__.__name__}.stack_size must be an int and greater than the quantity.')
        self.__stack_size = stack_size

    def pick_up(self, item: Self) -> Self | None:
        # If the items don't match, return the given item without modifications
        if self.object_type != item.object_type:
            return item

        # If the picked up quantity goes over the stack_size, add to make the quantity equal the stack_size
        if self.quantity + item.quantity > self.stack_size:
            item.quantity -= self.stack_size - self.quantity
            self.quantity = self.stack_size
            return item

        # Add the given item's quantity to the self item
        self.quantity += item.quantity

    def to_json(self) -> dict:
        data: dict = super().to_json()
        data['durability'] = self.durability
        data['value'] = self.value
        data['quantity'] = self.quantity
        data['stack_size'] = self.stack_size
        return data

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.durability: int | None = data['durability']
        self.value: int = data['value']
        self.quantity: int = data['quantity']
        self.stack_size: int = data['stack_size']
        return self

from game.common.enums import ObjectType
from game.common.game_object import GameObject
from typing import Self


class Item(GameObject):
    """
    Items have 4 different attributes: value, durability, quantity, stack-size.

    Value:
        The value of an item can be anything depending on the purpose of the game. For example, if a player can
        sell an item to a shop for gold/money, the value attribute would be used. However, this value may be used
        for anything to better fit the purpose of the game being created.

    ----------------------------------------------------------------------------------------------------------------

    Durability:
        The value of an item's durability can be either None or an integer.

        If durability is an integer, it allows for flexibility with the item. For example, if the durability is
        0, the item could disappear, "break," etc.

        If the durability is equal to None, it represents the item having infinite durability. In the case
        the game being created needs items without durability, set this attribute to None to prevent any difficulties.

    ----------------------------------------------------------------------------------------------------------------

    Quantity and Stack Size:
        These two work in tandem. Fractions (x/y) will be used to better explain the concept.

        Quantity simply refers to the amount of the current item the player has. For example, having 5 gold, 10
        gold, or 0 gold all work for representing the quantity.

        The stack_size represents how *much* of an item can be in a stack. Think of this like the Minecraft inventory
        system. For example, you can have 64 blocks of dirt, and if you were to gain one more, you would have a new
        stack starting at 1.

        In the case of items here, it works with the avatar.py file's inventory system (refer to those notes on how
        the inventory works in depth). The Minecraft analogy should help understand the concept.

        To better show this, quantity and stack size work like the following fraction model: quantity/stack_size.
        The quantity can never be 0 and must always be a minimum of 1. Furthermore, quantity cannot be greater than
        the stack_size. So 65/64 will not be possible.

    ----------------------------------------------------------------------------------------------------------------

    pick_up Method:

    
    """

    def __init__(self, value: int = 1, durability: int | None = 100, quantity: int = 1, stack_size: int = 1):
        super().__init__()
        self.__quantity = None  # This is here to prevent an error
        self.__durability = None  # This is here to prevent an error
        self.object_type: ObjectType = ObjectType.ITEM
        self.value: int = value  # Value can more specified based on purpose (e.g., the sell price)
        self.stack_size: int = stack_size  # the max quantity this item can contain
        self.durability: int | None = durability  # durability can be None to represent infinite durability
        self.quantity: int = quantity  # the current amount of this item

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
    def durability(self, durability: int | None):
        if durability is not None and not isinstance(durability, int):
            raise ValueError(f'{self.__class__.__name__}.durability must be an int or None.')
        if durability is not None and self.stack_size != 1:
            raise ValueError(
                f'{self.__class__.__name__}.durability must be set to None if stack_size is not equal to 1.')
        self.__durability = durability

    @value.setter
    def value(self, value: int) -> None:
        if value is None or not isinstance(value, int):
            raise ValueError(f'{self.__class__.__name__}.value must be an int.')
        self.__value: int = value

    @quantity.setter
    def quantity(self, quantity: int) -> None:
        if quantity is None or not isinstance(quantity, int):
            raise ValueError(f'{self.__class__.__name__}.quantity must be an int.')
        if quantity <= 0:
            raise ValueError(f'{self.__class__.__name__}.quantity must be greater than 0.')

        # The self.quantity is set to the lower value between stack_size and the given quantity
        # The remaining given quantity is returned if it's larger than self.quantity
        if quantity > self.stack_size:
            raise ValueError(f'{self.__class__.__name__}.quantity cannot be greater than '
                             f'{self.__class__.__name__}.stack_size')
        self.__quantity: int = quantity

    @stack_size.setter
    def stack_size(self, stack_size: int) -> None:
        if stack_size is None or not isinstance(stack_size, int):
            raise ValueError(f'{self.__class__.__name__}.stack_size must be an int.')
        if self.durability is not None and stack_size != 1:
            raise ValueError(f'{self.__class__.__name__}.stack_size must be 1 if {self.__class__.__name__}.durability '
                             f'is not None.')
        if self.__quantity is not None and stack_size < self.__quantity:
            raise ValueError(f'{self.__class__.__name__}.stack_size must be greater than or equal to the quantity.')
        self.__stack_size: int = stack_size

    def pick_up(self, item: Self) -> Self | None:
        if item is None or not isinstance(item, Item):
            raise ValueError(f'{item.__class__.__name__} is not of type Item.')

        # If the items don't match, return the given item without modifications
        if self.object_type != item.object_type:
            return item

        # If the picked up quantity goes over the stack_size, add to make the quantity equal the stack_size
        if self.quantity + item.quantity > self.stack_size:
            item.quantity -= self.stack_size - self.quantity
            self.quantity: int = self.stack_size
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

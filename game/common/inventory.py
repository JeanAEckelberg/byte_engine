from typing import Self

from game.common.enums import ObjectType
from game.common.game_object import GameObject
from game.common.items.item import Item

"""
Programmer's Notes:
What we are trying to do here is completely move the inventory methods out of avatar and into here. 
Here's a checklist of the functions we need to move.

- [ ]: Inventory getter and setter
- [ ]: Max inventory size
- [ ]: Held item (Should the index be in here or in avatar??)
- [ ]: Clean inventory (Can we make this happen automatically??)
- [ ]: Drop item from inventory
- [ ]: Take item from inventory
- [ ]: Pick up item
- [ ]: JSON serialization/deserialization functions

Maintained by: Mechanist (Dylan)
"""
class Inventory(GameObject):
    """
        This class represents the inventory of each avatar.
        This allows you to manipulate the inventory of each avatar.
    """
    __inventory_size: int = 50

    def __init__(self):
        super().__init__()
        self.object_type: ObjectType = ObjectType.INVENTORY

    def create_empty_inventory(self) -> list[Item | None]:
        return [None] * self.__inventory_size
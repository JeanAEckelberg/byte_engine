from game.common.map.occupiable import Occupiable
from game.common.enums import ObjectType
from typing import Self


class Tile(Occupiable):
    """
    `Tile Class Notes:`

        Tiles are used as a placeholder object when visualizing the GameBoard.

        Tile objects are never stored in the gameboard to ensure a faster generation.
        Since this is the case, if there is no GameObjectContainer at a specific coordinate, the visualizer will default
        to a tile sprite. Therefore, this file is still necessary for tile objects to be written to and from the json.
        ⚠️⚠️⚠️DO NOT DELETE THIS FILE⚠️⚠️⚠️
    """
    def __init__(self):
        super().__init__()
        self.object_type: ObjectType = ObjectType.TILE

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        return self

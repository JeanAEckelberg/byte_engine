import random
from typing import Self
from game.utils.vector import Vector
from game.common.avatar import Avatar
from game.common.game_object import GameObject
from game.common.map.tile import Tile
from game.common.map.wall import Wall
from game.common.enums import *


class GameBoard(GameObject):
    """
    Notes for creating the GameBoard:

    map_size:
        map_size is a Vector object, allowing you to specify the size of the x, y plane of the game board.
        For example, a Vector object with an 'x' of 5 and a 'y' of 7 will create a board 5 tiles wide and
        7 tiles long

    -----------------------------------------------------------------------------------------------------------

    locations:
        This is the bulkiest part of the generation. The locations field is a dictionary with a key
        being a list of Vectors, and the value being a list of GameObjects. This is used to assign the
        given GameObjects the given coordinates via the Vectors. This is done in two ways:

            Statically:
                If you want a GameObject to be at a specific coordinate, ensure that the key-value pair is
                ONE Vector and ONE GameObject.
                An example of this would be the following:
                    locations = {[vector_2_4] : [station_0]}

                In this example, vector_2_4 contains the coordinates (2, 4). (Note that this naming convention
                isn't necessary, but was used to help with the concept). Furthermore, station_0 is the
                GameObject that will be at coordinates (2, 4).

            Dynamically:
                If you want to assign multiple GameObjects to different coordinates, use a key-value
                pair of any length. However, the assignments will be random.
                An example of this would be the following:
                    locations =
                        {
                            [vector_0_0, vector_1_1, vector_2_2] : [station_0, station_1, station_2]
                        }

                When this is passed in, the three different vectors containing coordinates (0, 0), (1, 1), or
                (2, 2) will be randomly assigned station_0, station_1, or station_2.

                Therefore:
                If station_0 is at (1, 1),
                station_1 could be at (2, 2),
                then station_2 will be at (0, 0).

        Lastly, another example will be shown to explain that you can combine both static and
        dynamic assignments in the same dictionary:

            locations =
                {
                    [vector_0_0] : [station_0],
                    [vector_0_1] : [station_1],
                    [vector_1_1, vector_1_2, vector_1_3] : [station_2, station_3, station_4]
                }

        In this example, station_0 will be at vector_0_0 without interference. The same applies to
        station_1 and vector_0_1. However, for vector_1_1, vector_1_2, and vector_1_3, they will randomly
        be assigned station_2, station_3, and station_4.

    -----------------------------------------------------------------------------------------------------------

    walled:
        This is simply a bool value that will create a wall barrier on the boundary of the game_board. If
        walled is True, the wall will be created for you.

        For example, let the dimensions of the map be (5, 7). There will be wall Objects horizontally across
        x = 0 and x = 4. There will also be wall Objects vertically at y = 0 and y = 6.

        Below is a visual example of this, with 'x' being where the wall Objects are.

        x x x x x   y = 0
        x       x
        x       x
        x       x
        x       x
        x       x
        x x x x x   y = 6
    """

    def __init__(self, seed: int | None = None, map_size: Vector = Vector(),
                 locations: dict[[Vector]:[GameObject]] | None = None, walled: bool = False):

        super().__init__()
        self.seed = seed
        random.seed(seed)
        self.object_type: ObjectType = ObjectType.GAMEBOARD
        self.event_active = None
        self.map_size: Vector = map_size
        self.locations: dict = locations
        self.walled: bool = walled

        # game_map is initially going to be None. Since generation is slow, call generate_map() as needed
        self.game_map: list[list[GameObject]] | None = None

    @property
    def seed(self) -> int:
        return self.__seed

    @seed.setter
    def seed(self, seed: int | None):
        if seed is not None or not isinstance(seed, int):
            raise ValueError("Seed must be an integer.")
        self.__seed = seed

    @property
    def map_size(self) -> Vector:
        return self.__map_size

    @map_size.setter
    def map_size(self, map_size: Vector):
        if map_size is None or not isinstance(map_size, Vector):
            raise ValueError("Map_size must be a Vector.")
        self.__map_size = map_size

    @property
    def locations(self) -> dict:
        return self.__locations

    @locations.setter
    def locations(self, locations: dict[[Vector]:[GameObject]] | None):
        if locations is not None or not isinstance(locations, dict):
            raise ValueError("Locations must be a dict. The key must be a list of Vector Objects, and the "
                             "value a list of GameObject.")

        self.__locations = locations

    @property
    def walled(self) -> bool:
        return self.__walled

    @walled.setter
    def walled(self, walled: bool):
        if walled is None or not isinstance(walled, bool):
            raise ValueError("Walled must be a bool.")

        self.__walled = walled

    def generate_map(self):
        # generate map
        self.game_map = [[Tile() for _ in range(self.map_size.x)] for _ in range(self.map_size.y)]

        if self.walled:
            for x in range(self.map_size.x):
                if x == 0 or x == self.map_size.x - 1:
                    for y in range(self.map_size.y):
                        self.game_map[y][x].occupied_by = Wall()
                self.game_map[0][x].occupied_by = Wall()
                self.game_map[self.map_size.y - 1][x].occupied_by = Wall()

        self.__populate_map()

    def __populate_map(self):
        for k, v in self.locations.items():
            if len(k) != len(v) or (len(k) == 0 or len(v) == 0):  # Key-Value lengths must be > 0 and equal
                raise ValueError("A key-value pair from game_board.locations has mismatching lengths. "
                                 "They must be the same length, regardless of size.")
            j = random.choices(k, k=len(k))
            self.__help_populate(j, v)

    def __help_populate(self, vector_list: list[Vector], v: list[GameObject]):
        for i in v:
            temp_vector: Vector = vector_list.pop()

            if isinstance(i, Avatar):  # If the GameObject is an Avatar, assign it the coordinate position
                i.position = temp_vector

            temp_tile: GameObject = self.game_map[temp_vector.y][temp_vector.x]

            while hasattr(temp_tile.occupied_by, 'occupied_by'):
                temp_tile = temp_tile.occupied_by

            if temp_tile is not None:
                raise ValueError("Last item on the given tile doesn't have the 'occupied_by' attribute.")

            temp_tile.occupied_by = i

    def get_objects(self, look_for: ObjectType) -> list[GameObject]:
        to_return = list()

        for row in self.game_map:
            for object_in_row in row:
                temp: GameObject = object_in_row
                self.__get_objects_help(look_for, temp, to_return)

        return to_return

    @staticmethod
    def __get_objects_help(look_for: ObjectType, temp: GameObject | Tile, to_return: list[GameObject]):
        while hasattr(temp, 'occupied_by'):
            if temp.object_type is look_for:
                to_return.append(temp)

            # The final temp is the last occupied by option which is either an Avatar, Station, or None
            temp = temp.occupied_by

        if temp is not None and temp.object_type is look_for:
            to_return.append(temp)

    def to_json(self) -> dict:
        data: dict[str, str] = super().to_json()
        temp: list[list[GameObject]] = list((map(lambda tile: tile.to_json(), y)) for y in self.game_map)
        data["game_map"] = temp
        data["seed"] = self.seed
        data["map_size"] = self.map_size
        data["locations"] = self.locations
        data["walled"] = self.walled
        data['event_active'] = self.event_active
        return data

    def generate_event(self, start, end):
        self.event_active = random.randint(start, end)

    def from_json(self, data) -> Self:
        super().from_json(data)
        temp = data["game_map"]
        self.game_map: list[list[GameObject]] = list((map(lambda tile: Tile().from_json(tile), y)) for y in temp)
        self.seed: int | None = data["seed"]
        self.map_size: Vector = data["map_size"]
        self.locations: dict[[Vector]:[GameObject]] = data["locations"]
        self.walled: bool = data["walled"]
        self.event_active = data['event_active']
        return self

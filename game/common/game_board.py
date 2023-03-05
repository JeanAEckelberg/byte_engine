import random
from typing import Self
from game.utils.vector import Vector
from game.common.avatar import Avatar
from game.common.game_object import GameObject
from game.common.stations.station import Station
from game.common.stations.occupiable_station import Occupiable_Station
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
    def __init__(self, seed: int = None, map_size: Vector = Vector(),
                 locations: dict[[Vector]:[GameObject]] = None, walled: bool = False):

        random.seed(seed)
        super().__init__()
        self.object_type: ObjectType = ObjectType.GAMEBOARD
        self.event_active = None
        self.map_size: Vector = map_size
        self.locations: dict = locations
        self.walled: bool = walled

        # generate map
        # max_size(1) for x, and max_size(0)
        self.game_map = [[Tile() for x in range(self.map_size.y)] for y in range(self.map_size.x)]

        if walled:
            for x in range(self.map_size.x):
                if x == 0 or x == self.map_size.x-1:
                    for y in range(self.map_size.y):
                        self.game_map[y][x].occupied_by = Wall()
                self.game_map[0][x].occupied_by = Wall()
                self.game_map[self.map_size.y - 1][x].occupied_by = Wall()

    def populate_map(self):
        for k, v in self.locations.items():
            if len(k) != len(v) or (len(k) == 0 or len(v) == 0):  # Key-Value lengths must be > 0 and equal
                raise ValueError("A key-value pair from game_board.locations has mismatching lengths. "
                                 "They must be the same length, regardless of size.")
            j = random.choices(k, k=len(k))
            self.__help_populate(j, v)

    def __help_populate(self, j: Vector, v: list[GameObject]):
        for i in v:

            if isinstance(i, Avatar):  # If the GameObject is an Avatar, assign it the coordinate position
                i.position = j

            temp = self.game_map[j.y][j.x]

            while temp.occupied_by is not None:
                # if it's not none, and it doesn't have an occupied by attribute then its blocked and
                # movement fails
                if not hasattr(temp.occupied_by, 'occupied_by'):
                    raise Exception("The GameObject does not have an 'occupied_by' attribute.")

                temp = temp.occupied_by

            temp.occupied_by = i

    def stations(self) -> list:
        to_return = list()
        for row in self.game_map:
            for col in row:
                if isinstance(col.occupied_by, Station):
                    to_return.append(col.occupied_by)
                    self.__loop_occupied_by(col, to_return)
        return to_return

    def avatars(self) -> list:
        to_return = list()
        for row in self.game_map:
            for col in row:
                if isinstance(col.occupied_by, Avatar):
                    to_return.append(col.occupied_by)
                    self.__loop_occupied_by(col, to_return)
        return to_return

    def __loop_occupied_by(self, col: GameObject, to_return: list[GameObject]) -> None:
        # A helper method to be used in the stations and avatars methods.
        # Loops through the occupied_by chain and appends those Objects to the given list.
        while col.occupied_by:
            if hasattr(col.occupied_by, 'occupied_by'):
                to_return.append(col.occupied_by)


    def to_json(self) -> dict:
        data = super().to_json()
        temp = list([list(map(lambda tile: tile.to_json(), y)) for y in self.game_map])
        data["game_map"] = temp
        data['event_active'] = self.event_active
        return data

    def generate_event(self, start, end):
        self.event_active = random.randint(start, end)

    def from_json(self, data) -> Self:
        super().from_json(data)
        temp = data["game_map"]
        self.game_map = list([list(map(lambda tile: Tile().from_json(tile), y)) for y in temp])
        self.event_active = data['event_active']
        return self

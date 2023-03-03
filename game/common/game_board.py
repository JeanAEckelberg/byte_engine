import random
from game.common.avatar import Avatar
from game.common.game_object import GameObject
from game.common.stations.station import Station
from game.common.stations.occupiable_station import Occupiable_Station
from game.common.map.tile import Tile
from game.common.enums import *


class GameBoard(GameObject):
    def __init__(self, seed: int = None, map_size: (int, int) = tuple,
                 locations: dict = dict, walled: bool = False):

        random.seed(seed)
        super().__init__()
        self.object_type: ObjectType = ObjectType.GAMEBOARD
        self.event_active = None
        self.map_size: (int, int) = map_size
        self.locations: dict = locations
        self.walled: bool = walled

        """
        TODO: $  Type hint for constructor
        
        $  Get rid of station_hold and temp_pop_data
        $  Also get rid of the zipper for them
        $  Get rid of temp_hold
        
        $  Make sure that on line 39, where it says 13 and 7, that those are integers that can be passed in 
            to specify the size of the map
            
        $  Include in the constructor: Seed, a tuple of (y, x) to represent the map size, 
            dict of locations, and walled boolean
        
        $  Account for avatar being passed in the locations
        
        Account for stations with occupied_by as an attribute
        
        Needs extensive documentation on how the locations dict work
        
        Look at movement controller for how to get to top-most occupiable level
        
        $  Will have to modify cooks and ovens methods to be related to avatar and stations respectively 
        
        
        
        $  For the double for loop, check to make sure the key-value pairs have the same length, else 
            throw an error
            
        $  Check for Avatar in the value list of GameObjects to add the coordinates to the Avatar. This will be 
            its own unique check in the loops
            
        $  For the second for loop in the method, make a helper method that is used to avoid multiple 
            indents
        """

        # generate map
        # max_size(1) for x, and max_size(0)
        self.game_map = [[Tile() for x in range(self.map_size(1))] for y in range(self.map_size(0))]
        ####################
        ### If walled is true, make wall here
        ####################

    def populate_map(self):
        for k, v in self.locations.items():
            if len(k) != len(v) or (len(k) == 0 or len(v) == 0):  # Key-Value lengths must be > 0 and equal
                raise ValueError("A key-value pair from game_board.locations has mismatching lengths. "
                                 "They must be the same length, regardless of size.")
            j = random.choices(k, k=len(k))
            self.__help(j, v)

    def __help(self, j: (int, int), v: list[GameObject]):
        for i in v:
            (y, x) = j.pop()

            if isinstance(i, Avatar):  # If the GameObject is an Avatar, assign it the coordinate position
                i.position = j[::-1]

            self.game_map[y][x].occupied_by = i

    def stations(self) -> list:
        to_return = list()
        for row in self.game_map:
            for col in row:
                if isinstance(col.occupied_by, Station):
                    to_return.append(col.occupied_by)
        return to_return

    def avatars(self) -> list:
        to_return = list()
        for row in self.game_map:
            for col in row:
                if isinstance(col.occupied_by, Avatar):
                    to_return.append(col.occupied_by)
        return to_return

    def to_json(self):
        data = super().to_json()
        temp = list([list(map(lambda tile: tile.to_json(), y)) for y in self.game_map])
        data["game_map"] = temp
        data['event_active'] = self.event_active
        return data

    def generate_event(self, start, end):
        self.event_active = random.randint(start, end)

    def from_json(self, data):
        super().from_json(data)
        temp = data["game_map"]
        self.game_map = list([list(map(lambda tile: Tile().from_json(tile), y)) for y in temp])
        self.event_active = data['event_active']
        return self

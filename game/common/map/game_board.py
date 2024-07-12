import ast
import random
from typing import Self

from game.common.avatar import Avatar
from game.common.enums import *
from game.common.game_object import GameObject
from game.common.map.game_object_container import GameObjectContainer
from game.common.map.tile import Tile
from game.common.map.wall import Wall
from game.common.map.occupiable import Occupiable
from game.common.stations.occupiable_station import OccupiableStation
from game.common.stations.station import Station
from game.utils.vector import Vector


class GameBoard(GameObject):
    """
    `GameBoard Class Notes:`

    Map Size:
    ---------
        `map_size` is a Vector object, allowing you to specify the size of the (x, y) plane of the game board.
        For example, a Vector object with an 'x' of 5 and a 'y' of 7 will set a boarder of 5 tiles wide and
        7 tiles long.

        Example:
        ::
            _ _ _ _ _  y = 0
            |       |
            |       |
            |       |
            |       |
            |       |
            |       |
            _ _ _ _ _  y = 6

    -----

    Locations:
    ----------
        The locations field is a dictionary with a key of a vector with a value of GameObjectContainer.
        Every object in a GameObjectContainer will be store at the specified location.
        Each container will function like a stack, where you can only place a new object at the top of the stack.

    -----

    Walled:
    -------
        This is simply a bool value that will create a wall barrier on the boundary of the game_board. If
        walled is True, the wall will be generated.

        For example, let the dimensions of the map be (5, 7). There will be Wall objects horizontally across
        x = 0 and x = 4. There will also be Wall objects vertically at y = 0 and y = 6

        Below is a visual example of this, with 'x' being where the Wall objects are.

        Example:
        ::
            x x x x x   y = 0
            x       x
            x       x
            x       x
            x       x
            x       x
            x x x x x   y = 6
    """

    def __init__(self, seed: int | None = None, map_size: Vector = Vector(),
                 locations: dict[Vector, list[GameObject]] | None = None, walled: bool = False):

        super().__init__()
        # game_map is initially going to be None. Since generation is slow, call generate_map() as needed
        self.game_map: dict[Vector, GameObjectContainer] | None = None
        self.seed: int | None = seed
        random.seed(seed)
        self.object_type: ObjectType = ObjectType.GAMEBOARD
        self.event_active: int | None = None
        self.map_size: Vector = map_size
        # when passing Vectors as a tuple, end the tuple of Vectors with a comma, so it is recognized as a tuple
        self.locations: dict | None = locations
        self.walled: bool = walled

    @property
    def seed(self) -> int:
        return self.__seed

    @seed.setter
    def seed(self, seed: int | None) -> None:
        if self.game_map is not None:
            raise RuntimeError(f'{self.__class__.__name__} variables cannot be changed once generate_map is run.')
        if seed is not None and not isinstance(seed, int):
            raise ValueError(
                f'{self.__class__.__name__}.seed must be an int. '
                f'It is a(n) {seed.__class__.__name__} with the value of {seed}.')
        self.__seed = seed

    @property
    def game_map(self) -> dict[Vector, GameObjectContainer] | None:
        return self.__game_map

    @game_map.setter
    def game_map(self, game_map: dict[Vector, GameObjectContainer] | None) -> None:
        if game_map is not None and not isinstance(game_map, dict) \
                and any([not isinstance(vec, Vector) or not isinstance(go_container, GameObjectContainer)
                         for vec, go_container in game_map.items()]):
            raise ValueError(
                f'{self.__class__.__name__}.game_map must be a dict[Vector, GameObjectContainer].'
                f'It has a value of {game_map}.'
            )

        self.__game_map = game_map

    @property
    def map_size(self) -> Vector:
        return self.__map_size

    @map_size.setter
    def map_size(self, map_size: Vector) -> None:
        if self.game_map is not None:
            raise RuntimeError(f'{self.__class__.__name__} variables cannot be changed once generate_map is run.')
        if map_size is None or not isinstance(map_size, Vector):
            raise ValueError(
                f'{self.__class__.__name__}.map_size must be a Vector. '
                f'It is a(n) {map_size.__class__.__name__} with the value of {map_size}.')
        self.__map_size = map_size

    @property
    def locations(self) -> dict:
        return self.__locations

    @locations.setter
    def locations(self, locations: dict[Vector, list[GameObject]] | None) -> None:
        if self.game_map is not None:
            raise RuntimeError(f'{self.__class__.__name__} variables cannot be changed once generate_map is run.')
        if locations is not None and not isinstance(locations, dict):
            raise ValueError(
                f'Locations must be a dict. The key must be a tuple of Vector Objects, '
                f'and the value a list of GameObject. '
                f'It is a(n) {locations.__class__.__name__} with the value of {locations}.')

        self.__locations = locations

    @property
    def walled(self) -> bool:
        return self.__walled

    @walled.setter
    def walled(self, walled: bool) -> None:
        if self.game_map is not None:
            raise RuntimeError(f'{self.__class__.__name__} variables cannot be changed once generate_map is run.')
        if walled is None or not isinstance(walled, bool):
            raise ValueError(
                f'{self.__class__.__name__}.walled must be a bool. '
                f'It is a(n) {walled.__class__.__name__} with the value of {walled}.')

        self.__walled = walled

    def generate_map(self) -> None:
        """
        Populates the game map based off self.locations.
        :return: None
        """
        output: dict[Vector, GameObjectContainer] = dict()

        # Update all Avatar positions if they are to be placed on the map
        for vec, objs in self.locations.items():
            for obj in objs:
                if isinstance(obj, Avatar):
                    obj.position = vec

        if self.walled:
            # Generate the walls
            output.update({Vector(x=x, y=0): GameObjectContainer([Wall(), ]) for x in range(self.map_size.x)})
            output.update({Vector(x=x, y=self.map_size.y - 1): GameObjectContainer([Wall(), ])
                           for x in range(self.map_size.x)})
            output.update({Vector(x=0, y=y): GameObjectContainer([Wall(), ]) for y in range(1, self.map_size.y - 1)})
            output.update({Vector(x=self.map_size.x - 1, y=y): GameObjectContainer([Wall(), ])
                           for y in range(1, self.map_size.y - 1)})

        # convert locations dict to go_container
        output.update({vec: GameObjectContainer(objs) for vec, objs in self.locations.items()})
        self.game_map = output

    def get(self, coords: Vector) -> GameObjectContainer | None:
        """
        A GameObjectContainer object returned given the coordinates. If the coordinates are valid but are not in the
        game_map yet, a new GameObjectContainer is created and is stored in a new entry in the game_map dictionary.

        :param coords:
        :return: GameObjectContainer or None
        """
        if self.is_valid_coords(coords) and self.game_map.get(coords, None) is None:
            self.game_map[coords] = GameObjectContainer()

        return self.game_map.get(coords)

    def place(self, coords: Vector, game_obj: GameObject | None) -> bool:
        """
        Places the given object at the given coordinates if they are valid. A boolean is returned to represent a
        successful placement
        :param coords:
        :param game_obj:
        :return: True or False for a successful placement of the given object
        """
        return self.get(coords).place(game_obj) if self.is_valid_coords(coords) else False

    def get_objects_from(self, coords: Vector, object_type: ObjectType | None = None) -> list[GameObject]:
        """
        Returns a list of GameObjects from the given, valid coordinates. If an ObjectType is specified, only that
        ObjectType will be returned. If an ObjectType is not specified, the entire list of GameObjects will be
        returned. If nothing is found, an empty list is given.
        :param coords:
        :param object_type:
        :return: a list of GameObjects
        """
        return self.game_map[coords].get_objects(object_type) if coords in self.game_map else []

    def remove(self, coords: Vector, object_type: ObjectType) -> GameObject | None:
        """
        Removes the first instance of the given object type from the coordinates if they are valid. Returns None if
        invalid coordinates are given.
        :param coords:
        :param object_type:
        :return: GameObject or None
        """
        to_return: GameObject | None = self.game_map[coords].remove(object_type) if coords in self.game_map else None

        # if there is a None value paired with the coordinate key after removal, delete that entry from the dict
        if self.is_valid_coords(coords) and self.get(coords).get_top() is None:
            self.game_map.pop(coords, None)

        return to_return

    def get_top(self, coords: Vector) -> GameObject | None:
        """
        Returns the last object in the GameObjectContainer (i.e, the top-most object in the stack). Returns None if
        invalid coordinates are given.
        :param coords:
        :return: GameObject or None
        """
        return self.game_map[coords].get_top() if coords in self.game_map else None

    def object_is_found_at(self, coords: Vector, object_type: ObjectType) -> bool:
        """
        Searches for an object with the given object type at the given coordinate. If no object is found, or if the
        coordinate is invalid, return False.
        :param coords:
        :param object_type:
        :return: True or False to determine if the object is at that location
        """

        if not self.is_valid_coords(coords):
            return False

        result: list[GameObject] | None = self.game_map[coords].get_objects(object_type)
        return result is not None and len(result) > 0

    def is_valid_coords(self, coords: Vector) -> bool:
        """
        Check if the given coordinates are valid. In order to do so, the following criteria must be met:
            - The given coordinates must be in the self.game_map dictionary keys first
            - Otherwise, the coordinates must be within the size of the game map

        :param coords:
        :return: True if the coordinates are already in the map or are within the map size
        """

        return (0 <= coords.x < self.map_size.x) and (0 <= coords.y < self.map_size.y)

    def is_occupiable(self, coords: Vector) -> bool:
        return self.is_valid_coords(coords) and (self.get(coords).get_top() is None or
                                                 isinstance(self.get(coords).get_top(), Occupiable))

    # Returns the Vector and a list of GameObject for whatever objects you are trying to get
    # TODO: CHANGE RETURN TYPE TO BE A DICT NOT A LIST OF TUPLES
    def get_objects(self, look_for: ObjectType) -> list[tuple[Vector, list[GameObject]]]:
        """
        Zips together the game map's keys and values. A nested for loop then iterates through the zipped lists, and
        looks for any objects that have the same object type that was passed in. A list of tuples containing the
        coordinates and the objects found is returned. If the given object type isn't found on the map, then an empty
        list is returned
        """

        results: list[tuple[Vector, list[GameObject]]] = []

        # Loops through the zipped list
        # DICTIONARY COMPREHENSION HERE PLEASE
        for vec, go_container in self.game_map.items():
            found: list[GameObject] = go_container.get_objects(look_for)  # add the matching object to the found list

            # add values to result if something was found
            if len(found) > 0:
                results.append((vec, found))  # Add tuple pairings and objects found

        return results

    def to_json(self) -> dict:
        data: dict[str, object] = super().to_json()
        temp: dict[Vector, GameObjectContainer] | None = {str(vec.to_json()): go_container.to_json() for
                                                          vec, go_container in
                                                          self.game_map.items()} if self.game_map is not None else None
        data['game_map'] = temp
        data["seed"] = self.seed
        data["map_size"] = self.map_size.to_json()
        data["location_vectors"] = [vec.to_json() for vec in self.locations.keys()] if self.locations is not None \
            else None
        data["location_objects"] = [[obj.to_json() for obj in v] for v in
                                    self.locations.values()] if self.locations is not None else None
        data["walled"] = self.walled
        data['event_active'] = self.event_active
        return data

    def generate_event(self, start: int, end: int) -> None:
        self.event_active = random.randint(start, end)

    def __from_json_helper(self, data: dict) -> GameObject:
        temp: ObjectType = ObjectType(data['object_type'])
        match temp:
            case ObjectType.TILE:
                return Tile().from_json(data)
            case ObjectType.WALL:
                return Wall().from_json(data)
            case ObjectType.OCCUPIABLE_STATION:
                return OccupiableStation().from_json(data)
            case ObjectType.STATION:
                return Station().from_json(data)
            case ObjectType.AVATAR:
                return Avatar().from_json(data)
            # If adding more ObjectTypes that can be placed on the game_board, specify here
            case _:
                raise ValueError(
                    f'The object type of the object is not handled properly. The object type passed in is {temp}.')

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.seed: int | None = data["seed"]
        self.map_size: Vector = Vector().from_json(data["map_size"])

        self.locations: dict[Vector, list[GameObject]] = {
            Vector().from_json(k): [self.__from_json_helper(obj) for obj in v] for k, v in
            zip(data["location_vectors"], data["location_objects"])} if data["location_vectors"] is not None else None

        self.walled: bool = data["walled"]
        self.event_active: int = data['event_active']

        # json.ast.literal_eval is `abstract syntax tree`
        # the vector objects were stored as a dictionary in a string format
        # json.ast.literal_eval takes in the string, converts it to a dict, and uses that for the from_json()

        self.game_map: dict[Vector, GameObjectContainer] = {
            Vector().from_json(ast.literal_eval(k)): GameObjectContainer().from_json(v)
            for k, v in data['game_map'].items()} if data['game_map'] is not None else None

        return self

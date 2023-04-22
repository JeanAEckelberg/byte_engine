import unittest

from game.common.enums import ObjectType
from game.common.avatar import Avatar
from game.common.items.item import Item
from game.common.stations.station import Station
from game.common.stations.occupiable_station import Occupiable_Station
from game.common.map.tile import Tile
from game.common.map.wall import Wall
from game.utils.vector import Vector
from game.common.game_object import GameObject
from game.common.game_board import GameBoard

# class to test initalization of game_board
class TestGameBoard(unittest.TestCase):
    def setUp(self) -> None:
        self.item: Item = Item(10, None)
        self.wall: Wall = Wall()
        self.avatar: Avatar = Avatar(None, Vector(5, 5))
        self.locations: dict[tuple[Vector]:list[GameObject]] = {
            (Vector(1, 1),):[Station(None)],
            (Vector(1, 2), Vector(1, 3)):[Occupiable_Station(self.item), Station(None)],
            (Vector(5, 5),):[self.avatar],
            (Vector(5, 6),):[self.wall]
        }
        self.game_board: GameBoard = GameBoard(1, Vector(10, 10), self.locations, False)
        self.game_board.generate_map()

    # test that seed cannot be set after generate_map
    def test_seed_fail(self):
        with self.assertRaises(RuntimeError) as e:
            self.game_board.seed = 20
        self.assertEqual(str(e.exception), 'GameBoard variables cannot be changed once generate_map is run.')

    # test that map_size cannot be set after generate_map
    def test_map_size_fail(self):
        with self.assertRaises(RuntimeError) as e:
            self.game_board.map_size = Vector(1, 1)
        self.assertEqual(str(e.exception), 'GameBoard variables cannot be changed once generate_map is run.')
    
    # test that locations cannot be set after generate_map
    def test_locations_fail(self):
        with self.assertRaises(RuntimeError) as e:
            self.game_board.locations = self.locations
        self.assertEqual(str(e.exception), 'GameBoard variables cannot be changed once generate_map is run.')
    
    # test that locations raises RuntimeError even with incorrect data type
    def test_locations_incorrect_fail(self):
        with self.assertRaises(RuntimeError) as e:
            self.game_board.locations = Vector(1, 1)
        self.assertEqual(str(e.exception), 'GameBoard variables cannot be changed once generate_map is run.')
    
    # test that walled cannot be set after generate_map
    def test_walled_fail(self):
        with self.assertRaises(RuntimeError) as e:
            self.game_board.walled = False
        self.assertEqual(str(e.exception), 'GameBoard variables cannot be changed once generate_map is run.')
    
    # test that get_objects works correctly with stations
    def test_get_objects_station(self):
        stations: list[Station] = self.game_board.get_objects(ObjectType.STATION)
        self.assertTrue(all(map(lambda station: isinstance(station, Station), stations)))
        self.assertEqual(len(stations), 2)
        
    # test that get_objects works correctly with occupiable stations
    def test_get_objects_occupiable_station(self):
        occupiable_stations: list[Occupiable_Station] = self.game_board.get_objects(ObjectType.OCCUPIABLE_STATION)
        self.assertTrue(all(map(lambda occupiable_station: isinstance(occupiable_station, Occupiable_Station), occupiable_stations)))
        self.assertEqual(len(occupiable_stations), 1)

    # test that get_objects works correctly with avatar
    def testget_objects_avatar(self):
        avatars: list[Avatar] = self.game_board.get_objects(ObjectType.AVATAR)
        self.assertTrue(all(map(lambda avatar: isinstance(avatar, Avatar), avatars)))
        self.assertEqual(len(avatars), 1)

    # test that get_objects works correctly with walls
    def test_get_objects_wall(self):
        walls: list[Wall] = self.game_board.get_objects(ObjectType.WALL)
        self.assertTrue(all(map(lambda wall: isinstance(wall, Wall), walls)))
        self.assertEqual(len(walls), 1)

    # test json method
    def test_game_board_json(self):
        data: dict = self.game_board.to_json()
        temp: GameBoard = GameBoard().from_json(data)
        for (k, v), (x, y) in zip(self.locations.items(), temp.locations.items()):
            for (i, j), (a, b) in zip(zip(k, v), zip(x, y)):
                self.assertEqual(i.object_type, a.object_type)
                self.assertEqual(j.object_type, b.object_type)
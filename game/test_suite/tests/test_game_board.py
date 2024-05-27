import unittest

from game.common.enums import ObjectType
from game.common.avatar import Avatar
from game.common.items.item import Item
from game.common.stations.station import Station
from game.common.stations.occupiable_station import OccupiableStation
from game.common.map.wall import Wall
from game.utils.vector import Vector
from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard
import game.test_suite.utils


class TestGameBoard(unittest.TestCase):
    """
    `Test Gameboard Notes:`

        This class tests the different methods in the Gameboard class. This file is worthwhile to look at to understand
        the GamebBoard class better if there is still confusion on it.

        *This class tests the Gameboard specifically when the map is generated.*
    """

    def setUp(self) -> None:
        self.item: Item = Item(10, None)
        self.wall: Wall = Wall()
        self.avatar: Avatar = Avatar()
        self.locations: dict[Vector, list[GameObject]] = {
            Vector(0, 0): [Station(None)],
            Vector(1, 0): [OccupiableStation(self.item), Station(None)],
            Vector(2, 0): [OccupiableStation(self.item), OccupiableStation(self.item), OccupiableStation(self.item),
                           OccupiableStation(self.item)],
            Vector(0, 1): [self.avatar],
            Vector(1, 1): [self.wall],
        }

        self.game_board: GameBoard = GameBoard(1, Vector(3, 3), self.locations, False)
        self.game_board.generate_map()
        self.utils = game.test_suite.utils

    # test that seed cannot be set after generate_map
    def test_seed_fail(self):
        with self.assertRaises(RuntimeError) as e:
            self.game_board.seed = 20
        self.assertTrue(self.utils.spell_check(str(e.exception), 'GameBoard variables cannot be changed once '
                                                                 'generate_map is run.', False))

    # test that map_size cannot be set after generate_map
    def test_map_size_fail(self):
        with self.assertRaises(RuntimeError) as e:
            self.game_board.map_size = Vector(1, 1)
        self.assertTrue(self.utils.spell_check(str(e.exception), 'GameBoard variables cannot be changed once '
                                                                 'generate_map is run.', False))

    # test that locations cannot be set after generate_map
    def test_locations_fail(self):
        with self.assertRaises(RuntimeError) as e:
            self.game_board.locations = self.locations
        self.assertTrue(self.utils.spell_check(str(e.exception), 'GameBoard variables cannot be changed once '
                                                                 'generate_map is run.', False))

    # test that locations raises RuntimeError even with incorrect data type
    def test_locations_incorrect_fail(self):
        with self.assertRaises(RuntimeError) as e:
            self.game_board.locations = Vector(1, 1)
        self.assertTrue(self.utils.spell_check(str(e.exception), 'GameBoard variables cannot be changed once '
                                                                 'generate_map is run.', False))

    # test that walled cannot be set after generate_map
    def test_walled_fail(self):
        with self.assertRaises(RuntimeError) as e:
            self.game_board.walled = False
        self.assertTrue(self.utils.spell_check(str(e.exception), 'GameBoard variables cannot be changed once '
                                                                 'generate_map is run.', False))

    # test that get_objects works correctly with stations
    def test_get_objects_station(self):
        stations: list[tuple[Vector, list[GameObject]]] = self.game_board.get_objects(ObjectType.STATION)
        self.assertTrue(all(map(lambda station: isinstance(station[1][0], Station), stations)))
        self.assertEqual(len(stations), 2)

    # test that get_objects works correctly with occupiable stations
    def test_get_objects_occupiable_station(self):
        occupiable_stations: list[tuple[Vector, list[GameObject]]] = self.game_board.get_objects(
            ObjectType.OCCUPIABLE_STATION)
        self.assertTrue(
            all(map(lambda occupiable_station: isinstance(occupiable_station[1][0], OccupiableStation),
                    occupiable_stations)))
        objects_stacked = [x[1] for x in occupiable_stations]
        objects_unstacked = [x for xs in objects_stacked for x in xs]
        self.assertEqual(len(objects_unstacked), 5)

    def test_get_objects_occupiable_station_2(self):
        occupiable_stations: list[tuple[Vector, list[GameObject]]] = self.game_board.get_objects(
            ObjectType.OCCUPIABLE_STATION)

        # checks if the list of GameObjects has 4 OccupiableStations in that list
        self.assertTrue(any(map(lambda vec_list: len(vec_list[1]) == 4, occupiable_stations)))

        objects_stacked = [x[1] for x in occupiable_stations]
        objects_unstacked = [x for xs in objects_stacked for x in xs]
        self.assertEqual(len(objects_unstacked), 5)

    # test that get_objects works correctly with avatar
    def test_get_objects_avatar(self):
        avatars: list[tuple[Vector, list[GameObject]]] = self.game_board.get_objects(ObjectType.AVATAR)
        self.assertTrue(all(map(lambda avatar: isinstance(avatar[1][0], Avatar), avatars)))
        self.assertEqual(len(avatars), 1)

    # test that get_objects works correctly with walls
    def test_get_objects_wall(self):
        walls: list[tuple[Vector, list[GameObject]]] = self.game_board.get_objects(ObjectType.WALL)
        self.assertTrue(all(map(lambda wall: isinstance(wall[1][0], Wall), walls)))
        self.assertEqual(len(walls), 1)

    # testing a successful case of the place_on_top method
    def test_place_on_top_occupiable(self):
        success: bool = self.game_board.place_on_top(Vector(2, 0), Avatar())
        objects: list[GameObject] = self.game_board.game_map[Vector(2, 0)]

        # test return value is true
        self.assertTrue(success)

        # test all occupiable stations are still in the list
        [self.assertEqual(objects[x].object_type, ObjectType.OCCUPIABLE_STATION) for x in range(1, len(objects) - 1)]

        # test that the avatar is at the top of the list
        self.assertEqual(objects[-1].object_type, ObjectType.AVATAR)

    # testing another successful case of the place_on_top method
    def test_place_under_top_object(self):
        success: bool = self.game_board.place_on_top(Vector(0, 0), OccupiableStation())
        objects: list[GameObject] = self.game_board.game_map[Vector(0, 0)]

        # test return value is true
        self.assertTrue(success)

        # test that the UnoccupiableStation is first before the Station
        self.assertEqual(objects[0].object_type, ObjectType.OCCUPIABLE_STATION)
        self.assertEqual(objects[1].object_type, ObjectType.STATION)

    # testing a failing case of the place_on_top method
    def test_place_on_top_fail(self):
        before: list[GameObject] = self.game_board.game_map[Vector(0, 0)]

        success: bool = self.game_board.place_on_top(Vector(0, 0), Avatar())
        objects: list[GameObject] = self.game_board.game_map[Vector(0, 0)]

        # test return value is false
        self.assertFalse(success)

        # test that the list hasn't changed
        self.assertEqual(before, self.game_board.game_map[Vector(0, 0)])

    def test_get_objects_from(self):
        result: list[GameObject] = self.game_board.get_objects_from(Vector(2, 0), ObjectType.OCCUPIABLE_STATION)

        # check if the resulting lists are the same
        self.assertEqual(result, self.game_board.game_map[Vector(2, 0)])

    def test_get_objects_from_fail(self):
        result = self.game_board.get_objects_from(Vector(50, 0), ObjectType.OCCUPIABLE_STATION)
        self.assertEqual(result, None)

    def test_object_is_found_at(self):
        result: bool = self.game_board.object_is_found_at(Vector(0, 0), ObjectType.STATION)
        self.assertTrue(result)

    def test_object_is_found_at_fail(self):
        result: bool = self.game_board.object_is_found_at(Vector(0, 0), ObjectType.OCCUPIABLE_STATION)
        self.assertFalse(result)

    def test_get_all_objects_from(self):
        result: list[GameObject] = self.game_board.get_all_objects_from(Vector(0, 0))
        self.assertEqual(result, self.game_board.game_map[Vector(0, 0)])

    def test_get_all_objects_from_fail(self):
        result: list[GameObject] = self.game_board.get_all_objects_from(Vector(100, 0))
        self.assertEqual(result, None)

    # test json method
    def test_game_board_json(self):
        data: dict = self.game_board.to_json()
        temp: GameBoard = GameBoard().from_json(data)

        self.assertEqual(self.game_board.seed, temp.seed)
        self.assertEqual(self.game_board.map_size, temp.map_size)
        self.assertEqual(self.game_board.walled, temp.walled)
        self.assertEqual(self.game_board.event_active, temp.event_active)

        self.assertEqual(self.game_board.game_map.keys(), temp.game_map.keys())
        self.assertTrue(self.game_board.game_map.values(), temp.game_map.values())

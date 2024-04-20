import unittest

from game.common.avatar import Avatar
from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard
from game.common.stations.occupiable_station import OccupiableStation
from game.common.stations.occupiable_station_example import OccupiableStationExample
from game.common.stations.station import Station
from game.utils.vector import Vector
from game.common.enums import *


class TestOccupiable(unittest.TestCase):
    def test_on_top_of_stack(self) -> None:
        self.occ_station: OccupiableStation = OccupiableStation()
        self.station: Station = Station()
        self.avatar: Avatar = Avatar()

        self.locations: dict[tuple[Vector]: list[GameObject]] = {
            (Vector(1, 1),): [self.station, self.avatar, ],
        }
        self.game_board = GameBoard(0, Vector(4, 4), self.locations, True)  # create 4x4 gameboard
        self.game_board.generate_map()

        def test_place_up(self):
            self.assertTrue(isinstance(self.game_board.game_map[0][1].get_top_of_stack(ObjectType.WALL), Avatar))

        def test_place_down(self):
            self.assertTrue(isinstance(self.game_board.game_map[2][1].get_top_of_stack(ObjectType.OCCUPIABLE), Avatar))

        def test_place_left(self):
            self.assertTrue(isinstance(self.game_board.game_map[1][0].get_top_of_stack(ObjectType.WALL), Avatar))

        def test_place_right(self):
            self.assertTrue(isinstance(self.game_board.game_map[1][2].get_top_of_stack(ObjectType.OCCUPIABLE), Avatar))

        def test_on_wall(self):
            self.assertTrue(isinstance(self.game_board.game_map[1][1].get_top_of_stack(ObjectType.OCCUPIABLE), Avatar))

    def test_on_station(self) -> None:
        self.occ_station: OccupiableStation = OccupiableStation()
        self.station: Station = Station()
        self.avatar: Avatar = Avatar()

        self.locations: dict[tuple[Vector]: list[GameObject]] = {
            (Vector(1, 1),): [self.station, ],
            (Vector(1, 2),): [self.avatar, ],
        }

        self.game_board = GameBoard(0, Vector(4, 4), self.locations, True)  # create 4x4 gameboard
        self.game_board.generate_map()

        def test_on_occupiable_station(self):
            self.assertTrue(isinstance(self.game_board.game_map[2][2].get_top_of_stack(ObjectType.OCCUPIABLE_STATION),
                                       Avatar))

        def test_on_station(self):
            self.assertTrue(isinstance(self.game_board.game_map[1][1].get_top_of_stack(ObjectType.STATION), Avatar))

    def test_place_on_stack(self) -> None:
        pass

    def test_is_occupied_by_object_type(self) -> None:
        occ_station: OccupiableStation = OccupiableStation()
        station: Station = Station()

        occ_station.occupied_by = station
        self.assertTrue(occ_station.is_occupied_by_object_type(ObjectType.STATION))

    def test_is_occupied_by_game_obj(self) -> None:
        occ_station: OccupiableStation = OccupiableStation()
        station: Station = Station()

        occ_station.occupied_by = station
        self.assertTrue(occ_station.is_occupied_by_game_object(Station))

    # Remove Tests

    def test_remove_obj_type_from_occupied_by(self) -> None:
        occ_station: OccupiableStation = OccupiableStation()
        station: Station = Station()

        occ_station.occupied_by = station

        self.assertTrue(occ_station.is_occupied_by_object_type(ObjectType.STATION))

        occ_station.remove_object_type_from_occupied_by(ObjectType.STATION)

        self.assertFalse(occ_station.is_occupied_by_object_type(ObjectType.STATION))

    def test_remove_game_obj_from_occupied_by(self) -> None:
        occ_station: OccupiableStation = OccupiableStation()
        ex_occ_station: OccupiableStationExample = OccupiableStationExample()

        occ_station.occupied_by = ex_occ_station

        self.assertTrue(occ_station.is_occupied_by_game_object(OccupiableStationExample))

        self.assertEqual(occ_station.remove_game_object_from_occupied_by(ex_occ_station), ex_occ_station)

        self.assertFalse(occ_station.is_occupied_by_game_object(OccupiableStation))
        
    def test_remove_form_occupied_by_2_stack(self) -> None:
        occ_station: OccupiableStation = OccupiableStation()
        station: Station = Station()

        occ_station.occupied_by = station

        self.assertTrue(isinstance(occ_station.remove_game_object_from_occupied_by(station), Station))

    def test_remove_from_occupied_twice(self) -> None:
        station: OccupiableStation = OccupiableStation()
        station_1: OccupiableStation = OccupiableStation()

        # set occupied by order: station -> station 1
        station.occupied_by = station_1

        # Test that removing station works and that trying to remove it again returns None
        self.assertEqual(station.remove_object_type_from_occupied_by(ObjectType.OCCUPIABLE_STATION), station_1)

        self.assertEqual(station.remove_object_type_from_occupied_by(ObjectType.OCCUPIABLE_STATION), None)

    # test removing duplicate objects in the stack
    def test_remove_from_occupied_by_duplicates(self) -> None:

        station: OccupiableStation = OccupiableStation()
        station_1: OccupiableStation = OccupiableStation()
        station_2: OccupiableStation = OccupiableStation()
        station_3: OccupiableStation = OccupiableStation()

        # set occupied by order: station -> station 1 -> station 2 -> station 3
        station.occupied_by = station_1
        station_1.occupied_by = station_2
        station_2.occupied_by = station_3

        # test the stations are removed in the order: station 1 -> station 2 -> station 3
        self.assertEqual(station.remove_object_type_from_occupied_by(ObjectType.OCCUPIABLE_STATION), station_1)
        self.assertEqual(station.remove_object_type_from_occupied_by(ObjectType.OCCUPIABLE_STATION), station_2)
        self.assertEqual(station.remove_object_type_from_occupied_by(ObjectType.OCCUPIABLE_STATION), station_3)
        self.assertEqual(station.occupied_by, None)

    def test_remove_from_occupied_by_duplicates_2(self) -> None:
        occ_station1: OccupiableStation = OccupiableStation()
        occ_station2: OccupiableStation = OccupiableStation()
        occ_station3: OccupiableStation = OccupiableStation()
        station: Station = Station()

        # set occupied by order: station -> station 1 -> station 2 -> station 3
        occ_station1.occupied_by = occ_station2
        occ_station2.occupied_by = occ_station3
        occ_station3.occupied_by = station

        # test the stations are removed in the order: station 1 -> station 2 -> station 3
        self.assertEqual(occ_station1.remove_object_type_from_occupied_by(ObjectType.OCCUPIABLE_STATION), occ_station2)
        self.assertEqual(occ_station1.remove_object_type_from_occupied_by(ObjectType.OCCUPIABLE_STATION), occ_station3)
        self.assertEqual(occ_station1.remove_object_type_from_occupied_by(ObjectType.STATION), station)
        self.assertEqual(occ_station1.occupied_by, None)

    def test_is_occupied_by_game_object(self) -> None:
        occ_station: OccupiableStation = OccupiableStation()
        station: Station = Station()

        # set occupied by order: occ_station = station
        occ_station.occupied_by = station

        self.assertEqual(occ_station.remove_object_type_from_occupied_by(ObjectType.STATION), station)
        self.assertEqual(occ_station.occupied_by, None)

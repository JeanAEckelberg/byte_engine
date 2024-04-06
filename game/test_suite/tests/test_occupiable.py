import unittest

from game.common.avatar import Avatar
from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard
from game.common.stations.occupiable_station import OccupiableStation
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
        station: Station = Station()

        occ_station.occupied_by = station

        self.assertTrue(occ_station.is_occupied_by_game_object(Station))

        occ_station.remove_game_object_from_occupied_by(station)

        self.assertFalse(occ_station.is_occupied_by_game_object(Station))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    # NOTE: Test removing multiple objects at the same time from the occupiable stack
    # Also test removing ONE thing from a stack that has multiple things on it

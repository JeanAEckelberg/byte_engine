import unittest

from game.common.map.game_board import GameBoard
from game.controllers.movement_controller import MovementController
from game.common.stations.station import Station
from game.common.stations.occupiable_station import OccupiableStation
from game.common.map.wall import Wall
from game.utils.vector import Vector
from game.common.player import Player
from game.common.action import ActionType
from game.common.avatar import Avatar
from game.common.game_object import GameObject


class TestMovementControllerIfWall(unittest.TestCase):
    """
    `Test Movement Controller if Wall Notes:`

        This class tests the Movement Controller *specifically* for when there are walls -- or other impassable
        objects -- near the Avatar.
    """

    def setUp(self) -> None:
        self.movement_controller = MovementController()
        self.avatar = Avatar(Vector(2, 2), 1)
        self.locations: dict[tuple[Vector]: list[GameObject]] = {
            Vector(2, 1): [OccupiableStation()],
            Vector(1, 2): [Station()],
            Vector(3, 2): [Wall()],
            Vector(2, 2): [self.avatar],
            Vector(2, 3): [OccupiableStation(), Station()]
        }

        self.game_board = GameBoard(0, Vector(4, 4), self.locations, False)

        # test movements up, down, left and right by starting with default 3,3 then know if it changes from there \/
        self.client = Player(None, None, [], self.avatar)
        self.game_board.generate_map()

    # test move up
    def test_move_up(self):
        self.movement_controller.handle_actions(ActionType.MOVE_UP, self.client, self.game_board)
        self.assertEqual((str(self.client.avatar.position)), str(Vector(2, 1)))

    # test move down
    def test_move_down_on_occupied_occupiable_station_fail(self):
        self.movement_controller.handle_actions(ActionType.MOVE_DOWN, self.client, self.game_board)
        self.assertEqual((str(self.client.avatar.position)), str(Vector(2, 2)))

    # test move left
    def test_move_left_on_station_fail(self):
        self.movement_controller.handle_actions(ActionType.MOVE_LEFT, self.client, self.game_board)
        self.assertEqual((str(self.client.avatar.position)), str(Vector(2, 2)))

    # test moving off the map doesn't work
    def test_move_up_invalid_coordinate(self):
        self.movement_controller.handle_actions(ActionType.MOVE_UP, self.client, self.game_board)
        self.movement_controller.handle_actions(ActionType.MOVE_UP, self.client, self.game_board)
        self.movement_controller.handle_actions(ActionType.MOVE_UP, self.client, self.game_board)
        self.assertEqual((str(self.client.avatar.position)), str(Vector(2, 0)))

    def test_move_up_occupiable_station(self):
        self.movement_controller.handle_actions(ActionType.MOVE_UP, self.client, self.game_board)
        self.assertEqual(self.client.avatar.position, Vector(2, 1))

    def test_move_right_wall_fail(self):
        self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.client, self.game_board)
        self.assertEqual(self.client.avatar.position, Vector(2, 2))

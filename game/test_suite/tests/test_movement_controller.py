import unittest

from game.common.map.game_board import GameBoard
from game.controllers.movement_controller import MovementController
from game.utils.vector import Vector
from game.common.player import Player
from game.common.action import ActionType
from game.common.avatar import Avatar
from game.common.game_object import GameObject


class TestMovementController(unittest.TestCase):
    def setUp(self) -> None:
        self.movement_controller = MovementController()
        self.avatar = Avatar(None, Vector(1, 1), [], 1)
        self.locations: dict[tuple[Vector]: list[GameObject]] = {
            (Vector(1, 1),): [self.avatar]
        }
        self.game_board = GameBoard(0, Vector(3, 3), self.locations, True)
        self.client = Player(None, None, [], self.avatar)
        self.game_board.generate_map()

    def test_move_up(self):
        self.movement_controller.handle_actions(ActionType.MOVE_UP, self.client, self.game_board)
        self.assertEqual((str(self.client.avatar.position)), str(Vector(1, 0)))

    def test_move_left(self):
        self.movement_controller.handle_actions(ActionType.MOVE_LEFT, self.client, self.game_board)
        self.assertEqual((str(self.client.avatar.position)), str(Vector(0, 1)))

    def test_move_right(self):
        self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.client, self.game_board)
        self.assertEqual((str(self.client.avatar.position)), str(Vector(2, 1)))

    def test_move_down(self):
        self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.client, self.game_board)
        self.assertEqual((str(self.client.avatar.position)), str(Vector(1, 2)))



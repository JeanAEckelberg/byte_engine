import unittest

from game.common.enums import ObjectType
from game.common.avatar import Avatar
from game.common.items.item import Item
from game.common.stations.station import Station
from game.common.stations.occupiable_station import OccupiableStation
from game.common.map.tile import Tile
from game.common.map.wall import Wall
from game.utils.vector import Vector
from game.controllers.place_controller import *
from game.controllers.movement_controller import *


class place_controller(unittest.TestCase):
    def setUp(self) -> None:
        self.place_controller: PlaceController = PlaceController()
        self.movement_controller: MovementController = MovementController()

        self.avatar = Avatar(max_inventory_size=1)
        self.item: Item = Item()
        self.avatar.inventory = [self.item]
        self.client: Player = Player(avatar=self.avatar)
        self.avatar.held_item = self.item

        self.locations: dict[tuple[Vector]: list[GameObject]]={
            (Vector(1, 1), ): [self.avatar],
        }

        self.game_board = GameBoard(0, Vector(4, 4), self.locations, True)
        self.game_board.generate_map()

    def test_place_up(self) -> None:
        self.movement_controller.handle_actions(ActionType.MOVE_DOWN, self.client, self.game_board)
        self.place_controller.handle_actions(ActionType.PLACE_ITEM_UP, self.client, self.game_board)

        self.assertTrue(isinstance(self.game_board.game_map[1][1].occupied_by, Item))

    def test_place_down(self) -> None:
        self.place_controller.handle_actions(ActionType.PLACE_ITEM_DOWN, self.client, self.game_board)

        self.assertTrue(isinstance(self.game_board.game_map[2][1].occupied_by, Item))

    def test_place_left(self) -> None:
        self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.client, self.game_board)
        self.place_controller.handle_actions(ActionType.PLACE_ITEM_LEFT, self.client, self.game_board)

        self.assertTrue(isinstance(self.game_board.game_map[1][1].occupied_by, Item))

    def test_place_right(self) -> None:
        self.place_controller.handle_actions(ActionType.PLACE_ITEM_RIGHT, self.client, self.game_board)

        self.assertTrue(isinstance(self.game_board.game_map[1][2].occupied_by, Item))

from game.common.enums import *
from game.common.map.game_board import GameBoard
from game.common.map.tile import Tile
from game.common.player import Player
from game.controllers.controller import Controller
from game.utils.vector import Vector


class PlaceController(Controller):
    def __init__(self) -> None:
        super().__init__()

    def handle_actions(self, action: ActionType, client: Player, world: GameBoard):
        avatar_pos: Vector = client.avatar.position
        tile: Tile = world.game_map[avatar_pos.y][avatar_pos.x]

        pos_mod: Vector

        match action:
            case ActionType.PLACE_ITEM_CENTER:
                pos_mod = Vector(x=-0, y=0)
            case ActionType.PLACE_ITEM_UP:
                pos_mod = Vector(x=0, y=-1)
            case ActionType.PLACE_ITEM_DOWN:
                pos_mod = Vector(x=0, y=1)
            case ActionType.PLACE_ITEM_LEFT:
                pos_mod = Vector(x=-1, y=0)
            case ActionType.PLACE_ITEM_RIGHT:
                pos_mod = Vector(x=1, y=0)
            case _:
                return

        self.__place_item(client, tile, world, pos_mod)

    def __place_item(self, client: Player, tile: Tile, world: GameBoard, pos_mod: Vector) -> None:
        pass
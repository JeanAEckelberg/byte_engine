from game.common.enums import *
from game.common.avatar import Avatar
from game.common.items.item import Item
from game.common.player import Player
from game.controllers.controller import Controller
from game.common.map.game_board import GameBoard


class InventoryController(Controller):
    def __init__(self):
        super().__init__()

    def handle_actions(self, client: Player, world: GameBoard):
        # If a larger inventory is created, create more enums and add them here as needed
        item: Item
        avatar: Avatar = Player.avatar
        match client.action:
            case ActionType.SELECT_SLOT_0:
                item = avatar.inventory[0]
            case ActionType.SELECT_SLOT_1:
                item = avatar.inventory[1]
            case ActionType.SELECT_SLOT_2:
                item = avatar.inventory[2]
            case ActionType.SELECT_SLOT_3:
                item = avatar.inventory[3]
            case ActionType.SELECT_SLOT_4:
                item = avatar.inventory[4]
            case ActionType.SELECT_SLOT_5:
                item = avatar.inventory[5]
            case ActionType.SELECT_SLOT_6:
                item = avatar.inventory[6]
            case ActionType.SELECT_SLOT_7:
                item = avatar.inventory[7]
            case ActionType.SELECT_SLOT_8:
                item = avatar.inventory[8]
            case ActionType.SELECT_SLOT_9:
                item = avatar.inventory[9]
            case _:  # default case if it's not selecting an inventory slot
                return

        avatar.held_item = item

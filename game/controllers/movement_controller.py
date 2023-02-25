from game.controllers.controller import Controller
from game.common.enums import *


class MovementController(Controller):

    def __init__(self):
        super().__init__()
       
    def handle_actions(self, world, client):
        new_position = None
        avatar_x = client.cook.position[1]
        avatar_y = client.cook.position[0]
        match client.action.chosen_action:
            case ActionType.MOVE_UP:
                if not world.game_map[avatar_y - 1][avatar_x].occupied_by:
                    new_position = (avatar_y - 1, avatar_x)
            case ActionType.MOVE_DOWN:
                if not world.game_map[avatar_y + 1][avatar_x].occupied_by:
                    new_position = (avatar_y + 1, avatar_x)
            case ActionType.MOVE_LEFT:
                if not world.game_map[avatar_y][avatar_x - 1].occupied_by:
                    new_position = (avatar_y, avatar_x - 1)
            case ActionType.MOVE_RIGHT:
                if not world.game_map[avatar_y][avatar_x + 1].occupied_by:
                    new_position = (avatar_y, avatar_x + 1)
        # if client.action.chosen_action == ActionType.Move.up:
        #    if not world.game_map[avatar_y - 1][avatar_x].occupied_by:
        #       new_position = (avatar_y-1, avatar_x)
        # if client.action.chosen_action == ActionType.Move.down:
        #    if not world.game_map[avatar_y+1][avatar_x].occupied_by:
        #       new_position = (avatar_y+1, avatar_x)
        # if client.action.chosen_action == ActionType.Move.left:
        #    if not world.game_map[avatar_y][avatar_x-1].occupied_by:
        #       new_position = (avatar_y, avatar_x-1)
        # if client.action.chosen_action == ActionType.Move.right:
        #    if not world.game_map[avatar_y][avatar_x+1].occupied_by:
        #       new_position = (avatar_y, avatar_x+1)
        if new_position:
            world.game_map[avatar_y][avatar_x].occupied_by = None
            client.cook.position = new_position
            world.game_map[new_position[0]][new_position[1]].occupied_by = client.cook


        
                         
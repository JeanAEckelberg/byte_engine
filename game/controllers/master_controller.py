from copy import deepcopy
import random

from game.common.action import Action
from game.common.avatar import Avatar
from game.common.enums import *
from game.common.player import Player
# from game.common.stats import GameStats  - don't need it because it is specifically for 1.7
# but keeping it for now in case it breaks something
import game.config as config
from game.utils.thread import CommunicationThread
from game.controllers.movement_controller import MovementController
from game.controllers.controller import Controller
from game.controllers.interact_controller import InteractController


class MasterController(Controller):
    def __init__(self):
        super().__init__()
        self.game_over: bool = False
        # self.event_timer = GameStats.event_timer
        self.event_times: tuple[int, int] | None = None
        self.turn: int = 1
        self.current_world_data: GameBoard | None = None
        self.movement_controller: MovementController = MovementController()
        self.interact_controller: InteractController = InteractController()

    # Receives all clients for the purpose of giving them the objects they will control
    def give_clients_objects(self, clients: list(Player), world: GameBoard):
        # starting_positions = [[3, 3], [3, 9]]
        for index, client in enumerate(clients):
            client.avatar = Avatar(position=game_board[index])

    # Generator function. Given a key:value pair where the key is the identifier for the current world and the value is
    # the state of the world, returns the key that will give the appropriate world information
    def game_loop_logic(self, start=1):
        self.turn = start

        # Basic loop from 1 to max turns
        while True:
            # Wait until the next call to give the number
            yield str(self.turn)
            # Increment the turn counter by 1
            self.turn += 1

    # Receives world data from the generated game log and is responsible for interpreting it
    def interpret_current_turn_data(self, clients, world, turn):
        self.current_world_data = world
        if turn == 1:
            random.seed(world["seed"])
            self.event_times = random.randrange(162, 172), random.randrange(329, 339)

    # Receive a specific client and send them what they get per turn. Also obfuscates necessary objects.
    def client_turn_arguments(self, client, turn):
        turn_action = Action()
        client.action = turn_action

        # Create deep copies of all objects sent to the player
        current_world = deepcopy(self.current_world_data["game_map"])
        copy_avatar = deepcopy(client.avatar)
        # Obfuscate data in objects that that player should not be able to see
        # Currently world data isn't obfuscated at all
        args = (self.turn, turn_action, self.current_world_data)
        return args

    # Perform the main logic that happens per turn
    def turn_logic(self, clients, turn):
        for client in clients:
            self.movement_controller.handle_actions(self.current_world_data["game_map"], client)
            self.interact_controller.handle_actions(client, self.current_world_data["game_map"])
        # checks event logic at the end of round
        self.handle_events(clients)

    def handle_events(self, clients):
        # If it is time to run an event, master controller picks an event to run
        if self.turn == self.event_times[0] or self.turn == self.event_times[1]:
            self.current_world_data["game_map"].generate_event(EventType.example, EventType.example)
            # event type.example is just a placeholder for now

    # Return serialized version of game
    def create_turn_log(self, clients, turn):
        data = dict()
        data['tick'] = turn
        data['clients'] = [client.to_json() for client in clients]
        # Add things that should be thrown into the turn logs here
        data['game_map'] = self.current_world_data["game_map"].to_json()

        return data

    # Gather necessary data together in results file
    def return_final_results(self, clients, turn):
        data = dict()

        data['players'] = list()
        # Determine results
        for client in clients:
            data['players'].append(client.to_json())

        return data

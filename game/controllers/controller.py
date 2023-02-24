from game.common.enums import DebugLevel
from game.config import Debug


class Controller:

    def __init__(self):
        self.debug_level = DebugLevel.controller
        self.debug = False

    def handle_actions(self, client, world):
        return

    def print(self, *args):
        if self.debug and Debug.level >= self.debug_level:
            print(f'{self.__class__.__name__}: ', end='')
            print(*args)

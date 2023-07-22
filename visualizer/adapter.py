import random

import pygame
from visualizer.bytesprites.exampleTileBS import ExampleTileBS
from visualizer.bytesprites.exampleWallBS import ExampleWallBS
from visualizer.bytesprites.exampleBS import ExampleBS
from game.utils.vector import Vector
from visualizer.utils.text import Text
from visualizer.utils.button import Button


class Adapter:
    def __init__(self, screen):
        self.screen = screen
        self.bytesprites = []
        self.populate_bytesprite = pygame.sprite.Group()
        # create text and buttons here

    # define any methods button may run

    def on_event(self, event):
        # self.button.mouse_clicked(event)
        ...

    def prerender(self):
        ...

    def continue_animation(self):
        ...

    def recalc_animation(self, turn_log: dict):
        ...

    def populate_bytesprites(self) -> pygame.sprite.Group:
        # Instantiate all bytesprites for each object ands add them here
        self.populate_bytesprite.add(ExampleTileBS(self.screen))
        self.populate_bytesprite.add(ExampleWallBS(self.screen))
        self.populate_bytesprite.add(ExampleBS(self.screen))
        return self.populate_bytesprite.copy()

    def render(self):
        # self.button.render()
        # any logic for rendering text, buttons, and other visuals
        ...

    def clean_up(self):
        ...

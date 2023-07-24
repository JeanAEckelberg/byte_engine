import random

import pygame
from visualizer.bytesprites.exampleTileBS import ExampleTileBS
from visualizer.bytesprites.exampleWallBS import ExampleWallBS
from visualizer.bytesprites.exampleBS import ExampleBS
from game.utils.vector import Vector
from visualizer.utils.text import Text
from visualizer.utils.button import Button
from visualizer.utils.sidebars import Sidebars
from visualizer.bytesprites.bytesprite import ByteSprite


class Adapter:
    def __init__(self, screen):
        self.screen: pygame.Surface = screen
        self.bytesprites: list[ByteSprite] = []
        self.populate_bytesprite: pygame.sprite.Group = pygame.sprite.Group()

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
        # to access sidebars do sidebars.[whichever sidebar you are doing]
        ...

    def clean_up(self):
        ...

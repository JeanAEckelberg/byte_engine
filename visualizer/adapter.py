import random

import pygame
from typing import Callable, Any
from visualizer.bytesprites.exampleTileBS import ExampleTileBS
from visualizer.bytesprites.exampleWallBS import ExampleWallBS
from visualizer.bytesprites.exampleBS import ExampleBS
from game.utils.vector import Vector
from visualizer.utils.text import Text
from visualizer.utils.button import Button, ButtonColors
from visualizer.utils.sidebars import Sidebars
from visualizer.bytesprites.bytesprite import ByteSprite
from visualizer.templates.menu_templates import Basic


class Adapter:
    def __init__(self, screen):
        self.screen: pygame.Surface = screen
        self.bytesprites: list[ByteSprite] = []
        self.populate_bytesprite: pygame.sprite.Group = pygame.sprite.Group()
        self.menu = Basic(screen, 'Basic Title')
        self.turn_number = 0
        self.turn_max = 500

    # Define any methods button may run

    def start_menu_event(self, event: pygame.event) -> Any:
        return self.menu.start_events(event)

    def start_menu_render(self):
        self.menu.start_render()

    def on_event(self, event):
        # self.button.mouse_clicked(event)
        ...

    def prerender(self):
        ...

    def continue_animation(self):
        ...

    def recalc_animation(self, turn_log: dict):
        self.turn_number = turn_log['tick']

    def populate_bytesprites(self) -> pygame.sprite.Group:
        # Instantiate all bytesprites for each object ands add them here
        self.populate_bytesprite.add(ExampleTileBS(self.screen))
        self.populate_bytesprite.add(ExampleWallBS(self.screen))
        self.populate_bytesprite.add(ExampleBS(self.screen))
        return self.populate_bytesprite.copy()

    def render(self, sidebars: Sidebars) -> None:
        # self.button.render()
        # any logic for rendering text, buttons, and other visuals
        # to access sidebars do sidebars.[whichever sidebar you are doing]
        text = Text(sidebars.top, f'{self.turn_number} / {self.turn_max}', 48)
        text.rect.center = sidebars.top_rect.center
        text.render()

    def clean_up(self):
        ...

    def results_load(self, results: dict):
        self.menu.load_results_screen(results)

    def results_event(self, event: pygame.event) -> Any:
        return self.menu.results_events(event)

    def results_render(self):
        self.menu.results_render()


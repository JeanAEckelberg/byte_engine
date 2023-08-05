from typing import Any

import pygame

from game.utils.vector import Vector
from visualizer.utils.button import Button
from visualizer.utils.text import Text

"""
    This is file is for creating different templates for the start menu of the visualizer. Each different screen 
    will be a different class. The Basic class is the default template for the screen. Create extra classes for 
    different start menu screens. The Basic class can be used as a template on how to do so.
"""


class Basic:
    def __init__(self, screen: pygame.Surface, title: str):
        self.screen: pygame.Surface = screen
        self.title: Text = Text(screen, title, 48)
        self.title.rect.center = Vector.add_vectors(Vector(*self.screen.get_rect().center), Vector(0, -100)).as_tuple()
        # self.underline: Text = Text()
        self.start_button: Button = Button(screen, 'Start Game', lambda: False, font_size=24, padding=10)
        self.results_button: Button = Button(screen, 'Exit', lambda: False, font_size=24, padding=10)
        self.start_button.rect.center = Vector.add_vectors(Vector(*self.screen.get_rect().center),
                                                           Vector(0, 100)).as_tuple()

        self.results_button.rect.center = Vector.add_vectors(Vector(*self.screen.get_rect().center),
                                                             Vector(0, 100)).as_tuple()

        self.winning_team_name: Text = Text(screen, '', 0)

    def start_events(self, event: pygame.event) -> Any:
        return self.start_button.mouse_clicked(event) if self.start_button.mouse_clicked(
            event) is not None else lambda: True

    def start_render(self):
        self.title.render()
        self.start_button.render()

    def load_results_screen(self, results: dict):
        winning_team = max(results['players'], key=lambda x: x['avatar']['score'])
        self.winning_team_name = Text(self.screen, winning_team['team_name'], 36)
        self.winning_team_name.rect.center = self.screen.get_rect().center

    def results_events(self, event: pygame.event) -> Any:
        return self.results_button.mouse_clicked(event) if self.results_button.mouse_clicked(
            event) is not None else lambda: True

    def results_render(self):
        self.title.render()
        self.winning_team_name.render()
        self.results_button.render()

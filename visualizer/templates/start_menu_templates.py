import pygame
from typing import Callable, Any
from game.utils.vector import Vector
from visualizer.utils.text import Text
from visualizer.utils.button import Button, ButtonColors

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
        self.start_button: Button = Button(screen, 'Start Game', lambda: False, position=Vector(200, 200))

        temp_button = self.start_button.rect
        temp_button.center = Vector.add_vectors(Vector(*self.screen.get_rect().center),
                                                           Vector(0, 100)).as_tuple()
        self.start_button.position = Vector(*temp_button.topleft)

    def events(self, event: pygame.event) -> Any:
        return self.start_button.mouse_clicked(event) if self.start_button.mouse_clicked(event) is not None else lambda: True

    def render(self):
        self.title.render()
        self.start_button.render()



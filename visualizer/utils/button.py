import typing

import pygame
from visualizer.utils.text import Text
from game.utils.vector import Vector
from typing import Optional, Callable
from typing import TypeAlias

"""
Class that creates an intractable button extending the Text class.

Defaults same as defaults used in Text class.
Must give an action the button can perform upon being clicked
Can select three colors for both the text and button: default, mouse hover, and mouse clicked
Can also select padding for bg button and amount the border_radius for the bg button

Parameters:
Text               :  All parameters from the Text class (screen, text, font_size, font_name, fg_color, position)
action             :  Action performed when button is clicked
fg_color           :  Used to store default text color              Default - #daa520
fg_color_hover     :  Text color for hovering over button           Default - #fff000
fg_color_clicked   :  Text color for clicking button                Default - #1ceb42
bg_color           :  bg color default                              Default - #846311
bg_color_hover     :  bg color for hovering over button             Default - #936e13
bg_color_clicked   :  bg color for clicking button                  Default - #efb21b
padding            :  Amount of padding given to bg rect            Default - 5
border_radius      :  Level of smoothing to corners of button       Default - 5

In future projects, defaults for button style should be changed according to style of game for ease of code
"""

# typing alias for color
Color: TypeAlias = str | int | tuple[int, int, int, Optional[int]] | list[
    int, int, int, Optional[int]] | pygame.Color


class Button(Text):
    def __init__(self, screen: pygame.Surface, text: str, action: Callable,
                 font_size: int = 12,
                 font_name: str = 'bauhaus93',
                 fg_color: Color = pygame.Color('#daa520'),
                 fg_color_hover: Color = pygame.Color('#fff000'),
                 fg_color_clicked: Color = pygame.Color('#1ceb42'),
                 bg_color: Color = pygame.Color('#846311'),
                 bg_color_hover: Color = pygame.Color('#936e13'),
                 bg_color_clicked: Color = pygame.Color('#efb21b'),
                 padding: int = 5,
                 border_radius: int = 5,
                 position: Vector = Vector(0, 0)):
        super().__init__(screen, text, font_size, font_name, fg_color, position)
        self.fg_color: Color = self.color
        self.fg_color_hover: Color = fg_color_hover
        self.fg_color_clicked: Color = fg_color_clicked
        self.bg_color: Color = bg_color
        self.bg_color_hover: Color = bg_color_hover
        self.bg_color_clicked: Color = bg_color_clicked
        self.padding = padding
        self.border_radius = border_radius
        self.action: Callable = action
        self.mouse: pygame.mouse = pygame.mouse
        self.__bg_current_color = bg_color

    # getter methods
    @property
    def fg_color(self) -> Color:
        return self.__fg_color

    @property
    def fg_color_hover(self) -> Color:
        return self.__fg_color_hover

    @property
    def fg_color_clicked(self) -> Color:
        return self.__fg_color_clicked

    @property
    def bg_color(self) -> Color:
        return self.__bg_color

    @property
    def bg_color_hover(self) -> Color:
        return self.__bg_color_hover

    @property
    def bg_color_clicked(self) -> Color:
        return self.__bg_color_clicked

    @property
    def padding(self) -> int:
        return self.__padding

    @property
    def border_radius(self) -> int:
        return self.__border_radius

    @property
    def mouse(self) -> pygame.mouse:
        return self.__mouse

    @property
    def action(self) -> Callable:
        return self.__action

    # setter methods
    @fg_color.setter
    def fg_color(self, fg_color: Color) -> None:
        try:
            self.__fg_color: Color = pygame.Color(fg_color)
        except (ValueError, TypeError):
            raise ValueError(
                f'{self.__class__.__name__}.fg_color must be a one of the following types: str or int or tuple('
                f'int, int, int, [int]) or list(int, int, int, [int]) or pygame.Color.')

    @fg_color_hover.setter
    def fg_color_hover(self, fg_color_hover: Color) -> None:
        try:
            self.__fg_color_hover: Color = pygame.Color(fg_color_hover)
        except (ValueError, TypeError):
            raise ValueError(
                f'{self.__class__.__name__}.fg_color_hover must be a one of the following types: str or int or tuple('
                f'int, int, int, [int]) or list(int, int, int, [int]) or pygame.Color.')

    @fg_color_clicked.setter
    def fg_color_clicked(self, fg_color_clicked: Color) -> None:
        try:
            self.__fg_color_clicked: Color = pygame.Color(fg_color_clicked)
        except (ValueError, TypeError):
            raise ValueError(
                f'{self.__class__.__name__}.fg_color_clicked must be a one of the following types: str or int or tuple('
                f'int, int, int, [int]) or list(int, int, int, [int]) or pygame.Color.')

    @bg_color.setter
    def bg_color(self, bg_color: Color) -> None:
        try:
            self.__bg_color: Color = pygame.Color(bg_color)
        except (ValueError, TypeError):
            raise ValueError(
                f'{self.__class__.__name__}.bg_color must be a one of the following types: str or int or tuple('
                f'int, int, int, [int]) or list(int, int, int, [int]) or pygame.Color.')

    @bg_color_hover.setter
    def bg_color_hover(self, bg_color_hover: Color) -> None:
        try:
            self.__bg_color_hover: Color = pygame.Color(bg_color_hover)
        except (ValueError, TypeError):
            raise ValueError(
                f'{self.__class__.__name__}.bg_color_hover must be a one of the following types: str or int or tuple('
                f'int, int, int, [int]) or list(int, int, int, [int]) or pygame.Color.')

    @bg_color_clicked.setter
    def bg_color_clicked(self, bg_color_clicked: Color) -> None:
        try:
            self.__bg_color_clicked: Color = pygame.Color(bg_color_clicked)
        except (ValueError, TypeError):
            raise ValueError(
                f'{self.__class__.__name__}.bg_color_clicked must be a one of the following types: str or int or tuple('
                f'int, int, int, [int]) or list(int, int, int, [int]) or pygame.Color.')

    @padding.setter
    def padding(self, padding: int) -> None:
        if padding is None or not isinstance(padding, int):
            raise ValueError(f'{self.__class__.__name__}.padding must be an int.')
        self.__padding = padding

    @border_radius.setter
    def border_radius(self, border_radius: int) -> None:
        if border_radius is None or not isinstance(border_radius, int):
            raise ValueError(f'{self.__class__.__name__}.border_radius must be an int.')
        self.__border_radius = border_radius

    @mouse.setter
    def mouse(self, mouse: pygame.mouse) -> None:
        if mouse is None:
            raise ValueError(f'{self.__class__.__name__}.mouse must be of type pygame.mouse')
        self.__mouse: pygame.mouse = mouse

    @action.setter
    def action(self, action: Callable) -> None:
        print(action)
        if action is None or not isinstance(action, Callable):
            raise ValueError(f'{self.__class__.__name__}.action must be of type Callable')
        self.__action = action

    # methods

    # method to get the bg rect for the button
    def get_bg_rect(self) -> pygame.Rect:
        return pygame.Rect(
            [self.rect.x - self.padding, self.rect.y - self.padding, self.rect.width + (self.padding * 2),
             self.rect.height + (self.padding * 2)])

    # method that executes action parameter
    def execute(self, *args, **kwargs) -> any:
        return self.action(*args, **kwargs)

    # method for rendering button, called by render method in adapter class
    def render(self) -> None:
        # get bg_rect
        bg_rect: pygame.Rect = self.get_bg_rect()
        # hover logic for button
        self.color = self.fg_color
        self.__bg_current_color: Color = self.bg_color
        # if mouse position collides with rect, change to hover color
        if bg_rect.collidepoint(self.__mouse.get_pos()):
            self.color = self.fg_color_hover
            self.__bg_current_color = self.bg_color_hover
        pygame.draw.rect(self.screen, self.__bg_current_color, bg_rect, border_radius=self.border_radius)
        # render text on top of button
        super().render()

    # method for when button is clicked, called by on_event method in adapter
    def mouse_clicked(self, event: pygame.event) -> None:
        # get bg_rect
        bg_rect: pygame.Rect = self.get_bg_rect()
        # if both the mouse is hovering over the button and clicks, change color and execute self.action
        if bg_rect.collidepoint(self.__mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.color = self.fg_color_clicked
                self.__bg_current_color = self.bg_color_clicked
                self.execute()

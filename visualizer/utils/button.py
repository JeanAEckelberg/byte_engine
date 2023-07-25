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
Pass colors used for button using the ButtonColors class
Can also select padding for bg button and amount the border_radius for the bg button

Parameters for ButtonColor class:
fg_color           :  Used to store default text color              Default - #daa520
fg_color_hover     :  Text color for hovering over button           Default - #fff000
fg_color_clicked   :  Text color for clicking button                Default - #1ceb42
bg_color           :  bg color default                              Default - #846311
bg_color_hover     :  bg color for hovering over button             Default - #936e13
bg_color_clicked   :  bg color for clicking button                  Default - #efb21b

Parameters for Button class:
Text               :  All parameters from the Text class (screen, text, font_size, font_name, fg_color, position)
action             :  Action performed when button is clicked
colors             :  Of type ButtonColors, contains all colors used in Button class            Default - ButtonColors()
padding            :  Amount of padding given to bg rect                                        Default - 5
border_radius      :  Level of smoothing to corners of button                                   Default - 5
In future projects, defaults for button style should be changed according to style of game for ease of code
"""

# Typing alias for color
Color: TypeAlias = str | int | tuple[int, int, int, Optional[int]] | list[
    int, int, int, Optional[int]] | pygame.Color


# Class for colors used for button class
class ButtonColors:
    def __init__(self, fg_color: Color = pygame.Color('#daa520'),
                 fg_color_hover: Color = pygame.Color('#fff000'),
                 fg_color_clicked: Color = pygame.Color('#1ceb42'),
                 bg_color: Color = pygame.Color('#846311'),
                 bg_color_hover: Color = pygame.Color('#936e13'),
                 bg_color_clicked: Color = pygame.Color('#efb21b')):
        self.fg_color: Color = fg_color
        self.fg_color_hover: Color = fg_color_hover
        self.fg_color_clicked: Color = fg_color_clicked
        self.bg_color: Color = bg_color
        self.bg_color_hover: Color = bg_color_hover
        self.bg_color_clicked: Color = bg_color_clicked

    # Getter methods

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

    # Setter methods

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


class Button(Text):
    def __init__(self, screen: pygame.Surface, text: str, action: Callable,
                 font_size: int = 12,
                 font_name: str = 'bauhaus93',
                 colors: ButtonColors = ButtonColors(),
                 padding: int = 5,
                 border_radius: int = 5,
                 position: Vector = Vector(0, 0)):
        super().__init__(screen, text, font_size, font_name, colors.fg_color, position)
        self.colors = colors
        self.padding = padding
        self.border_radius = border_radius
        self.action: Callable = action
        # Get mouse used for interaction of buttons
        self.mouse: pygame.mouse = pygame.mouse
        # Set fg_color to color of text
        colors.fg_color = self.color
        # Set current bg color to bg color
        self.__bg_current_color = colors.bg_color
        # Set up counter system to display clicked colors
        self.__isClicked: float = 1000
        self.__clickedTime: float = 0

    # Getter methods

    @property
    def colors(self) -> ButtonColors:
        return self.__colors

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

    # Setter methods

    @colors.setter
    def colors(self, colors: ButtonColors) -> None:
        if colors is None or not isinstance(colors, ButtonColors):
            raise ValueError(f'{self.__class__.__name__}.colors must be of type ButtonColors')
        self.__colors = colors

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

    # Methods

    # Method to get the bg rect for the button
    def get_bg_rect(self) -> pygame.Rect:
        return pygame.Rect(
            [self.rect.x - self.padding, self.rect.y - self.padding, self.rect.width + (self.padding * 2),
             self.rect.height + (self.padding * 2)])

    # Method that executes action parameter
    def execute(self, *args, **kwargs) -> any:
        return self.action(*args, **kwargs)

    # Method for rendering button, called by render method in adapter class
    def render(self) -> None:
        # Count isClicked up by seconds
        self.__isClicked = pygame.time.get_ticks() - self.__clickedTime
        # Get bg_rect
        bg_rect: pygame.Rect = self.get_bg_rect()
        # Hover logic for button
        # If the clicked color has not been visible for ~1sec, do not change
        if self.__isClicked > 60:
            self.color = self.colors.fg_color
            self.__bg_current_color = self.colors.bg_color
            # If mouse position collides with rect, change to hover color
            if bg_rect.collidepoint(self.__mouse.get_pos()):
                self.color = self.colors.fg_color_hover
                self.__bg_current_color = self.colors.bg_color_hover
        pygame.draw.rect(self.screen, self.__bg_current_color, bg_rect, border_radius=self.border_radius)
        # Render text on top of button
        super().render()

    # Method for when button is clicked, called by on_event method in adapter
    def mouse_clicked(self, event: pygame.event) -> None:
        # Get bg_rect
        bg_rect: pygame.Rect = self.get_bg_rect()
        # If both the mouse is hovering over the button and clicks, change color and execute self.action
        if bg_rect.collidepoint(self.__mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.__isClicked = 0
                self.__clickedTime = pygame.time.get_ticks()
                self.color = self.colors.fg_color_clicked
                self.__bg_current_color = self.colors.bg_color_clicked
                self.execute()

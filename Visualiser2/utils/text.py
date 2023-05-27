import pygame
from game.utils.vector import Vector

"""
class that creates text to be displayed in the visualizer within a rectangle

defaults used unless otherwise stated:
font: Bauhaus93
color: #daa520          (yellowish)
position: Vector(0, 0)  (representing pixels on screen, top left pixel)
"""

class Text:
    def __init__(self, screen: pygame.Surface, text: str, font_size: int, font: str = 'bauhaus93', color: pygame.Color = pygame.Color('#daa520'), position: Vector = Vector(0, 0)):
        self.screen = screen                                    # screen used 
        self.font = pygame.font.SysFont(font, font_size)        # get font from list of SysFont, ajust size
        self.text_surface = self.font.render(text, True, color) # render text with color
        self.rect = self.text_surface.get_rect()                # get rectangle
        self.rect.topleft = position.as_tuple()                 # set top left position of rect to position

    # render text and rectangle to screen
    def render(self) -> None:
        self.screen.blit(self.text_surface, self.rect)

    # getter methods
    @property
    def screen(self) -> pygame.Surface:
        return self.__screen
    
    @property
    def text(self) -> str:
        return self.__text 
    
    @property
    def font(self) -> str:
        return self.__font
    
    @property
    def font_size(self) -> int:
        return self.__font_size
    
    @property
    def color(self) -> pygame.Color:
        return self.__color
    
    @property
    def position(self) -> Vector:
        return self.__position
    
    # setter methods
    @screen.setter
    def screen(self, screen: pygame.Surface) -> None:
        if screen is None or not isinstance(screen, pygame.Surface):
            raise ValueError(f'{self.__class__.__name__}.screen must be of type pygame.Surface.')
        self.__screen: pygame.Surface = screen

    @text.setter
    def text(self, text: str) -> None:
        if text is None or not isinstance(text, str):
            raise ValueError(f'{self.__class__.__name__}.text must be a str.')
        self.__text: str = text

    @font.setter
    def font(self, font: str) -> None:
        if font is None or not isinstance(font, str):
            raise ValueError(f'{self.__class__.__name__}.font must be a str.')
        self.__font: str = font

    @font_size.setter
    def font_size(self, font_size: int) -> None:
        if font_size is None or not isinstance(font_size, str):
            raise ValueError(f'{self.__class__.__name__}.font_size must be an int.')
        self.__font_size: int = font_size

    @color.setter
    def color(self, color: pygame.Color) -> None:
        if color is None or not isinstance(color, pygame.Color):
            raise ValueError(f'{self.__class__.__name__}.color must be of type pygame.Color.')
        self.__color: pygame.Color = color

    @position.setter
    def position(self, position: Vector) -> None:
        if position is None or not isinstance(position, Vector):
            raise ValueError(f'{self.__class__.__name__}.position must be a Vector.')
        self.__position: Vector = position
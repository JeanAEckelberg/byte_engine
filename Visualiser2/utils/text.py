import pygame
from game.utils.vector import Vector

class Text:
    def __init__(self, screen: pygame.Surface, text: str, font_size: int, font: str = 'bauhaus93', color: str = pygame.Color('#daa520'), position: Vector = Vector(0, 0)):
        self.screen = screen
        self.font = pygame.font.SysFont(font, font_size)
        self.text_surface = self.font.render(text, True, color)
        self.rect = self.text_surface.get_rect()
        self.rect.topleft = position.as_tuple()

    def render(self) -> None:
        self.screen.blit(self.text_surface, self.rect)
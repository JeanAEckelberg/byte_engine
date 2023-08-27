from dataclasses import dataclass
from typing import Any

import pygame

from game.utils.vector import Vector
from visualizer.utils.button import Button
from visualizer.utils.text import Text

"""
This file is for creating a default template for the playback implementation for the Visualizer. This will be displayed
while the game is running, with buttons including pause, speed up, slow down, restart, and save to mp4.
"""


@dataclass
class PlaybackButtons:
    pause_button: bool = False
    save_button: bool = False
    next_button: bool = False
    prev_button: bool = False
    start_button: bool = False
    end_button: bool = False
    normal_speed_button: bool = False
    fast_speed_button: bool = False
    fastest_speed_button: bool = False


class PlaybackTemplate:
    """
    Playback Template provides a menu of buttons during runtime of the visualizer to control the playback
    of the visualizer, including pausing, start, end, frame scrubbing, speeding up, and slowing down, as well as
    saving it to .mp4

    Buttons from this template are centered at the bottom of the screen, placed in three rows of three
    """

    def __init__(self, screen: pygame.Surface):
        self.screen: pygame.Surface = screen
        self.pause_button: Button = Button(self.screen, 'Pause', lambda: True, font_size=18)
        self.next_button: Button = Button(self.screen, 'Next', lambda: True, font_size=18)
        self.prev_button: Button = Button(self.screen, 'Prev', lambda: True, font_size=18)
        self.start_button: Button = Button(self.screen, 'Start', lambda: True, font_size=18)
        self.end_button: Button = Button(self.screen, 'End', lambda: True, font_size=18)
        self.save_button: Button = Button(self.screen, 'Save', lambda: True, font_size=18)
        self.normal_speed_button: Button = Button(self.screen, '1x', lambda: True, font_size=18)
        self.fast_speed_button: Button = Button(self.screen, '2x', lambda: True, font_size=18)
        self.fastest_speed_button: Button = Button(self.screen, '3x', lambda: True, font_size=18)

        self.prev_button.rect.center = Vector.add_vectors(Vector(*self.screen.get_rect().center),
                                                          Vector(-80, 225)).as_tuple()
        self.pause_button.rect.center = Vector.add_vectors(Vector(*self.screen.get_rect().center),
                                                           Vector(0, 225)).as_tuple()
        self.next_button.rect.center = Vector.add_vectors(Vector(*self.screen.get_rect().center),
                                                          Vector(80, 225)).as_tuple()
        self.start_button.rect.center = Vector.add_vectors(Vector(*self.screen.get_rect().center),
                                                           Vector(-80, 275)).as_tuple()
        self.save_button.rect.center = Vector.add_vectors(Vector(*self.screen.get_rect().center),
                                                          Vector(0, 275)).as_tuple()
        self.end_button.rect.center = Vector.add_vectors(Vector(*self.screen.get_rect().center),
                                                         Vector(80, 275)).as_tuple()
        self.normal_speed_button.rect.center = Vector.add_vectors(Vector(*self.screen.get_rect().center),
                                                                  Vector(-80, 325)).as_tuple()
        self.fast_speed_button.rect.center = Vector.add_vectors(Vector(*self.screen.get_rect().center),
                                                                Vector(0, 325)).as_tuple()
        self.fastest_speed_button.rect.center = Vector.add_vectors(Vector(*self.screen.get_rect().center),
                                                                   Vector(80, 325)).as_tuple()

    def playback_render(self) -> None:
        self.prev_button.render()
        self.pause_button.render()
        self.next_button.render()
        self.start_button.render()
        self.save_button.render()
        self.end_button.render()
        self.normal_speed_button.render()
        self.fast_speed_button.render()
        self.fastest_speed_button.render()

    def playback_events(self, event: pygame.event) -> PlaybackButtons:
        return PlaybackButtons(
            pause_button=self.pause_button.mouse_clicked(event),
            save_button=self.save_button.mouse_clicked(event),
            next_button=self.next_button.mouse_clicked(event),
            prev_button=self.prev_button.mouse_clicked(event),
            start_button=self.start_button.mouse_clicked(event),
            end_button=self.end_button.mouse_clicked(event),
            normal_speed_button=self.normal_speed_button.mouse_clicked(event),
            fast_speed_button=self.fast_speed_button.mouse_clicked(event),
            fastest_speed_button=self.fastest_speed_button.mouse_clicked(event))

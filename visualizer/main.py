import math
import sys
import os

import numpy
import pygame
import cv2
from PIL import Image

import game.config
from typing import Callable
from game.utils.vector import Vector
from visualizer.adapter import Adapter
from visualizer.bytesprites.bytesprite import ByteSprite
from visualizer.config import Config
from visualizer.utils.log_reader import logs_to_dict
from visualizer.templates.playback_template import PlaybackButtons
from threading import Thread


class ByteVisualiser:

    def __init__(self):
        pygame.init()
        self.config = Config()
        self.turn_logs: dict[str:dict] = {}
        self.size: Vector = self.config.SCREEN_SIZE
        self.tile_size: int = self.config.TILE_SIZE

        self.screen = pygame.display.set_mode(self.size.as_tuple())
        self.adapter = Adapter(self.screen)

        self.clock = pygame.time.Clock()

        self.tick: int = 0
        self.bytesprite_templates = pygame.sprite.Group()
        self.bytesprite_map: [[[ByteSprite]]] = list()

        self.default_frame_rate: int = self.config.FRAME_RATE

        self.playback_speed: int = 1
        self.paused: bool = False
        self.recording: bool = False

    def load(self):
        self.turn_logs = logs_to_dict()
        self.bytesprite_templates = self.adapter.populate_bytesprites()

    def prerender(self):
        self.screen.fill(self.config.BACKGROUND_COLOR)
        self.adapter.prerender()

    def render(self, button_pressed: PlaybackButtons) -> bool:
        # Run playback buttons method
        self.playback_controls(button_pressed)

        if self.tick % self.config.NUMBER_OF_FRAMES_PER_TURN == 0:
            # NEXT TURN
            if self.turn_logs.get(f'turn_{self.tick // self.config.NUMBER_OF_FRAMES_PER_TURN + 1:04d}') is None:
                return False
            self.recalc_animation(self.turn_logs[f'turn_{self.tick // self.config.NUMBER_OF_FRAMES_PER_TURN + 1:04d}'])
            self.adapter.recalc_animation(
                self.turn_logs[f'turn_{self.tick // self.config.NUMBER_OF_FRAMES_PER_TURN + 1:04d}'])
        else:
            # NEXT ANIMATION FRAME
            self.continue_animation()
            self.adapter.continue_animation()

        self.adapter.render()
        pygame.display.flip()

        # If recording, save frames into video
        if self.recording:
            self.save_video()
        self.tick += 1
        return True

    # Method to deal with playback_controls in visualizer (called in render method)
    def playback_controls(self, button_pressed: PlaybackButtons) -> None:
        # If recording, do not allow button to work
        if not self.recording:
            # Save button
            if PlaybackButtons.SAVE_BUTTON in button_pressed:
                self.recording = True
                self.playback_speed = 10
                self.tick = 0
            # Prev button to go back a frame
            if PlaybackButtons.PREV_BUTTON in button_pressed:
                whole, part = divmod(self.tick, self.config.NUMBER_OF_FRAMES_PER_TURN)
                self.tick = (whole - (0 if part > 0 else 1)) * self.config.NUMBER_OF_FRAMES_PER_TURN
            # Next button to go forward a frame
            if PlaybackButtons.NEXT_BUTTON in button_pressed:
                whole, part = divmod(self.tick, self.config.NUMBER_OF_FRAMES_PER_TURN)
                self.tick = (whole + (2 if part > 0 else 1)) * self.config.NUMBER_OF_FRAMES_PER_TURN
            # Start button to restart visualizer
            if PlaybackButtons.START_BUTTON in button_pressed:
                self.tick = 0
            # End button to end visualizer
            if PlaybackButtons.END_BUTTON in button_pressed:
                self.tick = self.config.NUMBER_OF_FRAMES_PER_TURN * (game.config.MAX_TICKS + 1)
            # Pause button to pause visualizer (allow looping of turn animation)
            if PlaybackButtons.PAUSE_BUTTON in button_pressed:
                self.paused = not self.paused
            if self.tick % self.config.NUMBER_OF_FRAMES_PER_TURN == 0 and self.paused:
                self.tick = max(self.tick - self.config.NUMBER_OF_FRAMES_PER_TURN, 0)
            if PlaybackButtons.NORMAL_SPEED_BUTTON in button_pressed:
                self.playback_speed = 1
            if PlaybackButtons.FAST_SPEED_BUTTON in button_pressed:
                self.playback_speed = 2
            if PlaybackButtons.FASTEST_SPEED_BUTTON in button_pressed:
                self.playback_speed = 4

    # Method to deal with saving game to mp4 (called in render if save button pressed)
    def save_video(self) -> None:
        # Convert to PIL Image
        new_image = pygame.image.tostring(self.screen.copy(), "RGBA", False)
        new_image = Image.frombytes("RGBA", self.screen.get_rect().size, new_image)
        # Scale image
        new_image.thumbnail(self.scaled)
        # Convert to OpenCV Image with numpy
        new_image = numpy.array(new_image)
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
        # Write image and go to next turn
        self.writer.write(new_image)

    def recalc_animation(self, turn_data: dict) -> None:
        """
        Determine what bytesprites are needed at which location and calls logic to determine active spritesheet and render
        :param turn_data: A dictionary of all the turn data for current turn
        :return: None
        """
        game_map: [[dict]] = turn_data['game_board']['game_map']
        # Iterate on each row on the game map
        row: list
        for y, row in enumerate(game_map):
            # Add rows to bytesprite_map if needed
            if len(self.bytesprite_map) < y + 1:
                self.bytesprite_map.append(list())
            # Iterate on each tile in the row
            tile: dict
            for x, tile in enumerate(row):
                # Add tiles to row if needed
                if len(self.bytesprite_map[y]) < x + 1:
                    self.bytesprite_map[y].append(list())
                # Render layers on tile
                temp_tile: dict | None = tile
                z: int = 0
                while temp_tile is not None:
                    # Add layers if needed
                    if len(self.bytesprite_map[y][x]) < z + 1:
                        self.bytesprite_map[y][x].append(None)

                    # Create or replace bytesprite at current tile on this current layer
                    if self.bytesprite_map[y][x][z] is None or self.bytesprite_map[y][x][z].object_type != temp_tile[
                        'object_type']:
                        if len(self.bytesprite_templates.sprites()) == 0:
                            raise ValueError(f'must provide bytesprites for visualization!')
                        sprite_class: ByteSprite | None = next(t for t in self.bytesprite_templates.sprites() if
                                                               isinstance(t, ByteSprite) and t.object_type == temp_tile[
                                                                   'object_type'])
                        # Check that a bytesprite template exists for current object type
                        if sprite_class is None:
                            raise ValueError(
                                f'Must provide a bytesprite for each object type! Missing object_type: {temp_tile["object_type"]}')

                        # Instantiate a new bytesprite on current layer
                        self.bytesprite_map[y][x][z] = sprite_class.__class__(self.screen)

                    # Call render logic on bytesprite
                    self.bytesprite_map[y][x][z].update(temp_tile, z, Vector(y=y, x=x))
                    # increase iteration
                    temp_tile = temp_tile.get('occupied_by') if temp_tile.get(
                        'occupied_by') is not None else temp_tile.get('held_item')
                    z += 1

                # clean up additional layers
                while len(self.bytesprite_map[y][x]) > z:
                    self.bytesprite_map[y][x].pop()

    def continue_animation(self) -> None:
        row: list
        tile: list
        sprite: ByteSprite
        [[[sprite.set_image_and_render() for sprite in tile] for tile in row] for row in self.bytesprite_map]

    def postrender(self):
        self.adapter.clean_up()
        self.clock.tick(self.default_frame_rate * self.playback_speed)

    def loop(self):

        thread: Thread = Thread(target=self.load)
        thread.start()

        # Start Menu loop
        in_phase: bool = True
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: sys.exit()
                    if event.key == pygame.K_RETURN: in_phase = False

                if in_phase:
                    in_phase = self.adapter.start_menu_event(event)

            self.adapter.start_menu_render()

            pygame.display.flip()

            if not in_phase:
                break
            self.clock.tick(self.default_frame_rate * self.playback_speed)

        thread.join()

        size = (self.config.SCREEN_SIZE.x, self.config.SCREEN_SIZE.y)
        self.scaled = (math.ceil(size[0] / 2), math.ceil(size[1] / 2))
        self.writer = cv2.VideoWriter("out.mp4", cv2.VideoWriter_fourcc(*'H264'), self.default_frame_rate, self.scaled)

        in_phase: bool = True

        while True:
            playback_buttons: PlaybackButtons = PlaybackButtons(0)
            # pygame events used to exit the loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: sys.exit()
                    if event.key == pygame.K_RETURN: in_phase = False

                playback_buttons = self.adapter.on_event(event)

            self.prerender()

            if in_phase:
                in_phase = self.render(playback_buttons)

            if not in_phase:
                break
            self.postrender()

        # Results
        in_phase = True
        self.adapter.results_load(self.turn_logs['results'])
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: sys.exit()
                    if event.key == pygame.K_RETURN: in_phase = False

                if in_phase:
                    in_phase = self.adapter.results_event(event)

            self.adapter.results_render()

            pygame.display.flip()

            if self.recording:
                self.save_video()

            if not in_phase:
                break
            self.clock.tick(math.floor(self.default_frame_rate * self.playback_speed))

        if self.recording:
            self.writer.release()
        sys.exit()


if __name__ == '__main__':
    byte_visualiser: ByteVisualiser = ByteVisualiser()
    byte_visualiser.loop()

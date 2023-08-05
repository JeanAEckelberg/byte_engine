import sys

import pygame
from typing import Callable
from game.utils.vector import Vector
from visualizer.adapter import Adapter
from visualizer.bytesprites.bytesprite import ByteSprite
from visualizer.config import Config
from visualizer.utils.log_reader import logs_to_dict
from visualizer.utils.sidebars import Sidebars
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
        self.sidebars: Sidebars = Sidebars()

    def load(self):
        self.turn_logs = logs_to_dict()
        self.bytesprite_templates = self.adapter.populate_bytesprites()

    def prerender(self):
        self.screen.fill(self.config.BACKGROUND_COLOR)
        self.sidebars.top.fill(self.config.BACKGROUND_COLOR)
        self.sidebars.bottom.fill(self.config.BACKGROUND_COLOR)
        self.sidebars.left.fill(self.config.BACKGROUND_COLOR)
        self.sidebars.right.fill(self.config.BACKGROUND_COLOR)
        self.adapter.prerender()

    def render(self) -> bool:
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

        self.adapter.render(self.sidebars)
        self.screen.blit(self.sidebars.top, self.sidebars.top_rect)
        self.screen.blit(self.sidebars.bottom, self.sidebars.bottom_rect)
        self.screen.blit(self.sidebars.left, self.sidebars.left_rect)
        self.screen.blit(self.sidebars.right, self.sidebars.right_rect)
        pygame.display.flip()
        self.tick += 1
        return True

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
        self.clock.tick(self.config.FRAME_RATE)

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
            self.clock.tick(self.config.FRAME_RATE)

        thread.join()

        in_phase = True
        while True:
            # pygame events used to exit the loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: sys.exit()
                    if event.key == pygame.K_RETURN: in_phase = False

                self.adapter.on_event(event)

            self.prerender()

            if in_phase:
                in_phase = self.render()

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

            if not in_phase:
                break
            self.clock.tick(self.config.FRAME_RATE)

        sys.exit()


if __name__ == '__main__':
    byte_visualiser: ByteVisualiser = ByteVisualiser()
    byte_visualiser.loop()

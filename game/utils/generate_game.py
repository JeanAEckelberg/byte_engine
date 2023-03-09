import random

from game.config import *
from game.utils.helpers import write_json_file
from game.common.game_board import GameBoard


def generate(seed: int = random.randint(0, 1000000000)):
    print('Generating game map...')

    temp = GameBoard(seed)
    temp.generate_map()
    data = temp.to_json()

    # for x in range(1, MAX_TICKS + 1):
    #     data[x] = 'data'


    # Verify logs location exists
    if not os.path.exists(GAME_MAP_DIR):
        os.mkdir(GAME_MAP_DIR)

    # Write game map to file
    write_json_file(data, GAME_MAP_FILE)

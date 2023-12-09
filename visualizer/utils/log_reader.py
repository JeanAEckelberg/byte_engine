import os
from pathlib import Path
import game.config as gc
import json


def logs_to_dict(log_dir: str | None) -> dict:
    temp: dict = {}
    print(os.getcwd())
    for file in Path(gc.LOGS_DIR if log_dir is None else log_dir).glob('*.json'):
        with open(file, 'r') as f:
            temp[file.stem] = json.load(f)
    print(temp)
    return temp

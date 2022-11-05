import json
import pathlib

def load_config():
    with pathlib.Path('config.json').open() as data_file:
        config = json.load(data_file)

    return config

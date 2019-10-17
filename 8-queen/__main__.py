import yaml
import os
from pdb import set_trace

import numpy as np
from scipy.spatial import distance
from queens import Queens

def load_config(dir, config='config.yml'):
    """ Loads a yaml config file

    Args:
        file (str): The location of yml file that needs to be loaded.

        config (str): The name of the config file to be loaded.

    Returns:
        A dictionary based on the yml file.
    """
    file_ = os.path.join(dir, config)

    with open(file_, 'r') as stream:
        try:
            params = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    return params


if __name__ == "__main__":
    # Load config parameters
    working_dir = os.getcwd()
    config = load_config(dir=working_dir, config='config.yml')
    params = config['queens']

    queens = Queens(n=params['n'])
    queens.populate_board()
    queens.print_board()
    queens.neighbors()
    set_trace()

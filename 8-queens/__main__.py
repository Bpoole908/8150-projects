import yaml
import os
from pdb import set_trace

import numpy as np

from queens import Queens
from hill_climbing import HillClimbing

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

def basic_stats(queens, epochs=1):
    """ Wrapper for HillClimbing.basic to calculate stats based on a 
        given number of epochs.

        Args:
            queens (Queens): Queens object used in hill climbing algorithm.

            epochs (int): Number of epochs to run before calculating averages.
    
    """
    successes = {'count': np.finfo(float).eps, 'steps' : 0}
    failures = {'count': np.finfo(float).eps, 'steps' : 0} 

    for e in range(epochs):
        print("{:=^50d}".format(e+1))
        # New random board
        queens.populate_board(seed=None)

        successful, steps = HillClimbing.basic(queens)

        if successful:
            successes['count'] += 1
            successes['steps'] += steps
        else:
            failures['count'] += 1
            failures['steps'] += steps

    print("{:=^50s}".format("Stats"))
    print("Success Stats")
    print("-Rate: {:.2f}".format(successes['count'] / epochs))
    print("-Steps: {:.2f}".format(successes['steps'] / successes['count']))
    print("Failure Stats")
    print("-Rate: {:.2f}".format(failures['count'] / epochs))
    print("-Steps: {:.2f}".format(failures['steps'] / failures['count']))

def sideways_moves_stats(queens, threshold=100, epochs=1):
    """ Wrapper for HillClimbing.sideways_moves to calculate stats based on a 
        given number of epochs.

    Args:
        queens (Queens): Queens object used in hill climbing algorithm.

        threshold (int): Threshold number sideways moves allowed.

        epochs (int): Number of epochs to run before calculating averages.
    
    """
    successes = {'count': np.finfo(float).eps, 'steps' : 0}
    failures = {'count': np.finfo(float).eps, 'steps' : 0} 

    for e in range(epochs):
        print("{:=^50d}".format(e+1))
        # New random board
        queens.populate_board(seed=None)

        successful, steps = HillClimbing.sideways_moves(queens, threshold)

        if successful:
            successes['count'] += 1
            successes['steps'] += steps
        else:
            failures['count'] += 1
            failures['steps'] += steps

    print("{:=^50s}".format("Stats"))
    print("Success Stats")
    print("-Rate: {:.2f}".format(successes['count'] / epochs))
    print("-Steps: {:.2f}".format(successes['steps'] / successes['count']))
    print("Failure Stats")
    print("-Rate: {:.2f}".format(failures['count'] / epochs))
    print("-Steps: {:.2f}".format(failures['steps'] / failures['count']))

def random_restarts_stats(queens, threshold=100, epochs=1):
    """ Wrapper for HillClimbing.random_restarts to calculate stats based on a 
        given number of epochs.

        Args:
            queens (Queens): Queens object used in hill climbing algorithm.

            threshold (int): Threshold number sideways moves allowed.

            epochs (int): Number of epochs to run before calculating averages.
    
    """
    successes = {'count': np.finfo(float).eps, 'steps' : 0, 'restarts': 0}
    failures = {'count': np.finfo(float).eps, 'steps' : 0, 'restarts': 0} 

    for e in range(epochs):
        print("{:=^50d}".format(e+1))
        # New random board
        queens.populate_board(seed=None)

        successful, steps, restarts = HillClimbing.random_restarts(
            queens=queens, threshold=threshold)

        if successful:
            successes['count'] += 1
            successes['steps'] += steps
            successes['restarts'] += restarts
        else:
            failures['count'] += 1
            failures['steps'] += steps
            failures['restarts'] += restarts

    print("{:=^50s}".format("Stats"))
    print("Success Stats")
    print("-Rate: {:.2f}".format(successes['count'] / epochs))
    print("-Steps: {:.2f}".format(successes['steps'] / successes['count']))
    print("-Restarts: {:.2f}".format(successes['restarts'] / successes['count']))
    print("Failure Stats")
    print("-Rate: {:.2f}".format(failures['count'] / epochs))
    print("-Steps: {:.2f}".format(failures['steps'] / failures['count']))
    print("-Restarts: {:.2f}".format(failures['restarts'] / failures['count']))
  
if __name__ == "__main__":
    # Load config parameters
    working_dir = os.getcwd()
    config = load_config(dir=working_dir, config='config.yml')
    params = config['queens']

    # Initialize 8-queens problem 
    queens = Queens(n=params['n'])
    queens.populate_board(seed=params['seed'])

    # Select algorithm to use based on config file
    if params['htype'].lower() == 'basic':
        basic_stats(queens=queens, epochs=params['epochs'])
    elif params['htype'].lower() == 'sideways':
        sideways_moves_stats(
            queens=queens, threshold=params['sideways_moves'],
            epochs=params['epochs'])
    elif params['htype'].lower() == 'random-restarts':
        random_restarts_stats(
            queens=queens, threshold=params['sideways_moves'],
            epochs=params['epochs'])
    else:
        raise ValueError("Invalid htype given!")


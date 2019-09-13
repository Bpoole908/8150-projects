import yaml
import os
from pdb import set_trace

import numpy as np
from scipy.spatial import distance
from a_star import AStar

def load_config(dir, config='config.yml'):
    """ Loads a yaml config file

    Args:
        file (str): The location of yml file that needs to be loaded.

    Returns:
        Returns a dictionary based on the yml file.
    """

    file = os.path.join(dir, config)
    with open(file, 'r') as stream:
        try:
            params = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return params

def duplicate_check(a):
    """ Check for duplicate values in a ndarray 
    
        Args:
            a (ndarray): Array to be checked for duplicate values.
    """
    if len(np.unique(a.flatten())) != len(a.flatten()):
        raise Exception("Duplicate numbers detected! Check initial and goal states!") 

def solvable(state, goal):
    """ Determine if any 8-puzzle game is solvable.
    
        In order for this check to work with any goal I map all goals to the base 
        number system. Once the mapping in place I check the number of inversions
        (total amount of numbers that are out of order). If the inversions are 
        even then the problem is solvable otherwise the problem is not solvable.

        Example:
            base = [1,2,3,4,5,6,7,8]
            goal = [8,7,6,5,4,3,2,1]
            mapped = {8: 1, 7: 2, 6: 3, 5: 4, 4: 5, 3: 6, 2: 7, 1: 8}

        Args:
            state (ndarray): Initial state.

            goal (ndarray): Goal state.
        
        Returns:
            Returns true the the number of inversions is even (solvable) and
            false if the number of inversions is odd (not solvable).
    """
    base = [1,2,3,4,5,6,7,8]
    invs = 0
    state = state[state != 0]
    goal = goal[goal != 0]
    mapped = {g: b for g, b in zip(goal, base)}
    state = state.ravel()

    for ii, i  in enumerate(state):
        print(i)
        print(state[ii+1:])
        for j in state[ii+1:]:
            if mapped[i]>mapped[j]: 
                invs += 1
        print("Inversions: {}".format(invs))

    return (invs%2 == 0)

if __name__ == "__main__":
    working_dir = os.getcwd()
    config = load_config(dir=working_dir, config='config.yml')
    init_state = np.array(config['a_star']['init_state'])
    goal_state = np.array(config['a_star']['goal_state'])

    print("Initial state:\n{}".format(init_state))
    duplicate_check(init_state)
    print("Goal state:\n{}".format(goal_state))
    duplicate_check(goal_state)
    print("="*50)

    can_solve = solvable(init_state, goal_state)
    if not can_solve:
        print("WARNING: CANT SOLVE THIS PUZZLE!")
        set_trace()

    a_star =  AStar(init_state=init_state, goal_state=goal_state)
    a_star.solve()
    pass

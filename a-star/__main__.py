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
            state (ndarray): Initial state to test.

            goal (ndarray): Goal state, i.e. desired number system.
        
        Returns:
            Returns true the the number of inversions is even (solvable) and
            false if the number of inversions is odd (not solvable).
    """
    base = [1,2,3,4,5,6,7,8] # base number system to map to
    invs = 0 # Total number of inversions  

    # Remove blanks (i.e. 0's) from the state and flaten to a vector
    state = state[state != 0]
    state = state.ravel() 

    # Remove blanks (i.e. 0's) from the goal
    goal = goal[goal != 0] 

    # Map goal number system to base number system
    mapped = {g: b for g, b in zip(goal, base)} 

    # Calculate inversions 
    print("Key: {}".format(goal))
    for ii, i  in enumerate(state):
        i_invs = 0
        print("Checking {} against {}...".format(i, state[ii+1:]))
        for j in state[ii+1:]:
            if mapped[i]>mapped[j]: 
                i_invs += 1
        invs += i_invs
        print("{} has {} inversions ".format(i, invs))
    print("Total inversions: {}".format(invs))

    return (invs%2 == 0)

def misplaced(state, goal):
    """ Calculates the total number of numbers out of place.

        Finds the total number of mismatches between the state and goal.

        Args:
            state (ndarray): Current state

            goal (ndarray): Goal state

        Returns:
            An interger valued heuristic representing the number of out of place
            numbers (tiles) with respect to the goal state. 
    """

    return  np.count_nonzero(state-goal)

def manhattan(state, goal):
    """ Calculates the manhattan distance given two states.

        Finds the coordinates of all numbers (tiles) in the state and goal. The 
        absolute difference between the state's and goal's corresponding numbers
        is then computed and summed.

        Args:
            state (ndarray): Current state

            goal (ndarray): Goal state

        Returns:
            An interger valued heuristic representing the sum of all the numbers
            distances (city block distance) from their goal position.
    """
    distance = 0

    for i in range(1, len(state.ravel())):
        state_coords = np.hstack(np.where(state == i))
        goal_coords = np.hstack(np.where(goal == i))

        distance += np.abs(state_coords - goal_coords).sum() 

    return distance

if __name__ == "__main__":
    # Load config parameters
    working_dir = os.getcwd()
    config = load_config(dir=working_dir, config='config.yml')
    init_state = np.array(config['a_star']['init_state'])
    goal_state = np.array(config['a_star']['goal_state'])
    
    # Determine which heuristic to use
    if config['a_star']['heuristic'] == "manhattan":
        heuristic = manhattan
    elif config['a_star']['heuristic'] == "misplaced":
        heuristic = misplaced
    else:
        raise ValueError("Heuristic name invalid!")

    # Print initial and goal state
    print("Initial state:\n{}".format(init_state))
    duplicate_check(init_state)
    print("Goal state:\n{}".format(goal_state))
    duplicate_check(goal_state)
    print("="*50)

    # Test if A* problem is solvable
    can_solve = solvable(init_state, goal_state)
    print("="*50)
    if can_solve:
        print("PUZZLE IS SOLVABLE!")
    else:
        print(
            "WARNING: PUZZLE IS NOT SOLVABLE!\n"
            "Enter `c` to proceed.\n" 
            "Doing so will search the entire state space!",
            "This will take a long time and is not advised...")
        set_trace()

    # Init and run A* solver
    print("="*50)
    a_star =  AStar(init_state=init_state, goal_state=goal_state)
    a_star.solve(heuristic=heuristic)

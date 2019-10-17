import numpy as np
from queens import Queens

def random_minimum_neighbor(conflicts):
    """ Randomly selects neighbor from equally minimal neighbors.

        Args:
            conflicts (list): List of intergets holding the conflicts for each
                neighbor generated. 
    """
    np.random.seed(None)
    min_conflict = np.min(conflicts)
    min_conflict_locs = np.where(conflicts == min_conflict)[0]
    # print("choices: {}".format(len(min_conflict_locs)))

    return np.random.choice(min_conflict_locs, 1)[0]

class HillClimbing(object):

    @staticmethod
    def basic(queens):
        """ Basic hill climbing algorithm that terminates on increased heuristic 
            (conflicts) and will randomly select from equally minimal neighbors.

            Args:
                queens (Queens): Queens object for N-queens problem.
            
            Returns:
                True or False if a solution was found or not and the number of 
                steps it took.
        """
        steps = 0
        queens.print_board()
        print("conflicts: {}".format(queens.heuristic()))

        while True:
            steps += 1
            current_h = queens.heuristic()
            neighbors, conflicts = queens.neighbors()

            # Find the neighbor with the smallest amount of conflicts (h) 
            min_idx = random_minimum_neighbor(conflicts)
            next_state = queens.coords_to_board(neighbors[min_idx])
            next_state_h = conflicts[min_idx]

            # Print board and stats    
            queens.board = next_state
            queens.print_board()
            print("conflicts: {}".format(next_state_h))
            print("step: {}".format(steps))

            if next_state_h == 0:
                print("SUCCESS!")
                return True, steps
            if next_state_h >= current_h:
                print("FAILED!")
                return False, steps

    @staticmethod
    def sideways_moves(queens, threshold=100):
        """ Sideways move hill climbing algorithm that terminates when the 
            sideways move threshold is exceeded. This algorithm will also 
            randomly select from equally minimal neighbors. Setting the 
            threshold parameter to 1 is the same as running the basic method.

            Args:
                queens (Queens): Queens object for N-queens problem.

                threshold (int): Number of sideways steps allowed.
            
            Returns:
                True or False if a solution was found or not and the number of 
                steps it took.
        """
        side_counter = 0
        steps = 0
        queens.print_board()
        print("conflicts: {}".format(queens.heuristic()))

        while True:
            steps += 1
            current_h = queens.heuristic()
            neighbors, conflicts = queens.neighbors()

            # Find the neighbor with the smallest amount of conflicts (h) 
            min_idx = random_minimum_neighbor(conflicts)
            next_state = queens.coords_to_board(neighbors[min_idx])
            next_state_h = conflicts[min_idx]

            # Increase or reset side was moves base on equality
            if next_state_h == current_h:
                side_counter += 1
            elif next_state_h < current_h:
                side_counter = 0

            queens.board = next_state
            queens.print_board()
            print("conflicts: {}".format(next_state_h))
            print("step: {}".format(steps))
            print("sideways move: {}".format(side_counter))
        
            # Success check
            if next_state_h == 0:
                print("SUCCESS!")
                return True, steps
            # Failure check
            if next_state_h > current_h :
                print("FAILED!")
                return False, steps
            # Sideways move check
            if side_counter >= threshold:
                print("FAILED!")
                return False, steps

    @staticmethod
    def random_restarts(queens, threshold=100):
        """ Random restart hill climbing algorithm that restarts at random 
            initializes when no solution could previously be found. By default this 
            algorithm uses sideways moves but can be disabled by setting threshold to 
            1. This algorithm will also randomly select from equally minimal neighbors.

            Args:
                queens (Queens): Queens object for N-queens problem.

                threshold (int): Number of sideways steps allowed.
            
            Returns:
                True or False if a solution was found or not, the number of 
                steps it took, and the number of restarts.
        """
        restarts = 0
        
        while True:
            successful, steps = HillClimbing.sideways_moves(queens, threshold)
            if successful:
                print("total restarts: {}".format(restarts))
                return successful, steps, restarts
            else:
                restart_string = "Restart {}".format(restarts)
                print("{:-^50s}".format(restart_string))
                queens.populate_board(seed=None)
                restarts += 1
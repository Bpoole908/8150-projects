from queue import PriorityQueue
from pdb import set_trace

import numpy as np

class PuzzleNode(object):
    """ Represents a state/node in the 8-puzzle problem.

        Attributes:
            state (ndarray): Current state of the 8-puzzle board.

            parent (PuzzleNode): Parent of the current state.

            g (int): G-score of the current state.

            h (int): H-score of the current state.

            f (int): F-score of the current state.
    """
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0
    
    def equals(self, other):
        """ Checks equality of Numpy ndarrays. 
        
            Args:
                other (ndarray): Another ndarray to check equality with.
        """
        return (self.state == other).all()

    def move(self, row_empty, col_empty, row_new, col_new):
        """ Executes a desired move on the current state.

            Args.
                row_empty (int): Current row location of the 0.

                col_empty (int): Current column location fo the 0.

                row_new (int): The row the 0 is moving to.

                col_new (int): The column the 0 is moving to.

            Returns:
                A new state represented by an ndarray.
        """
        child_state = self.state.copy()
        tmp = self.state[row_new, col_new]
        child_state[row_new, col_new] = 0
        child_state[row_empty,col_empty] = tmp

        return child_state
    
    def generate_children(self):
        """ Generates all the possible children for the current state. 

            This is down by considering all the valid moves that are avaliable 
            to the current state. When a move is executed the move() method is 
            called to generate a new child state representation.

            Returns:
                A list of children represented as ndarrays.
        """
        children = []
        # Corrodents of the empty block corresponding to row x col
        empty_coord = np.hstack(np.where(self.state == 0))

        # Attempt to move left
        left = empty_coord - [0, 1] 
        if left[1] >= 0:
            #print("move left")
            child_state = self.move(*empty_coord, *left)
            children.append(PuzzleNode(state=child_state, parent=self))
        # Attempt to move right
        right = empty_coord + [0, 1] 
        if right[1] < self.state.shape[1]:
            #print("move right")
            child_state = self.move(*empty_coord, *right)
            children.append(PuzzleNode(state=child_state, parent=self))
        ## Attempt to move right
        up = empty_coord - [1, 0] 
        if up[0] >= 0:
            #print("move up")
            child_state = self.move(*empty_coord, *up)
            children.append(PuzzleNode(state=child_state, parent=self))
        # Attempt to move down
        down = empty_coord + [1, 0] 
        if down[0] < self.state.shape[0]:
            #print("move down")
            child_state = self.move(*empty_coord, *down)
            children.append(PuzzleNode(state=child_state, parent=self))
        
        return children

class AStar(object):
    """ A* algorithm for solving graph and pathing problems.

        Attributes:
            init (ndarray): Initial state the algorithm will state in.

            goal (ndarray): Goal state the algorithm needs to find.
    """ 
    def __init__(self, init_state, goal_state):
        self.init = init_state
        self.goal = goal_state
 
    def solve(self, heuristic):
        """ Attempts to solve problem using the A* algorithm.

            Notes:
                Once A* has found a solution it will print the required steps
                along with the h, g, and f scores for each step. If the problem 
                is not solvable the program will attempt to iterate over the
                entire state space.
            
            Args:
                heuristic (func): A heuristic function thats input is the goal state.

            Returns:
                A boolean where a true value corresponds to solving the problem
                while false corresponds to an unsolvable problem.
        """
        open_set = [] # frontier
        closed_set = [] # explored
        generated = 0

        # Init state node object
        current_node = PuzzleNode(state=self.init, parent=None)

        # Init start nodes scores
        current_node.g = 0
        current_node.h = heuristic(self.init, self.goal)
        current_node.f = current_node.g + current_node.h
        current_node.parent = None

        # Add node to open_set
        open_set.append(current_node)
        while open_set:
            # Sort nodes then remove smallest score node adding it to the closed set
            print("Openset size: {}".format(len(open_set)), end="\r")
            open_set.sort(key= lambda x: x.f, reverse=True)
            current_node = open_set.pop()
            closed_set.append(current_node)
        
            # Goal check
            if current_node.equals(self.goal):
                self.print_solution(current_node) # output solution
                print("Nodes Expanded: {}".format(len(closed_set)))
                print("Nodes generated: {}".format(generated))
                return True

            # Generate current nodes children and loop through them
            children = current_node.generate_children()
            generated += len(children)
            for child in children:
                if any(child.equals(n.state) for n in closed_set):
                    continue
                
                child.g =  current_node.g + 1
                child.h = heuristic(child.state, self.goal)
                child.f = child.g + child.h
                child.parent = current_node

                # Don't add child if it already exists and is more expensive.
                if any(child.equals(n.state) and child.g > n.g for n in open_set):
                    continue

                # Add child
                # assert child.h + 1 >= current_node.h
                open_set.append(child)

        return False

    def print_solution(self, current_node, step=0):
        """ Prints solution recursively.

            Args:

                current_node (ndarray): Current state of the solution

                step (int): Counts the total number of steps it takes to reach
                the initial state from the goal state.
            
            Return:
                The total steps it took to reach the initial state by recursively
                iterating from the goal state to the initial state.
        """
        if current_node.parent is None:
            print("Step {}\n{}".format(0, current_node.state))
            print("{} = {} + {}\n".format(current_node.f, current_node.g, current_node.h))
            return step

        total_steps = self.print_solution(current_node.parent, step=step+1)
        print("Step {}\n{}".format(total_steps - step, current_node.state))
        print("{} = {} + {}\n".format(current_node.f, current_node.g, current_node.h))

        return total_steps

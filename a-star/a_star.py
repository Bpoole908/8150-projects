from queue import PriorityQueue
from pdb import set_trace

import numpy as np 

def array_check(a):
    if not isinstance(a, np.ndarray):
        raise ValueError("Input is not a numpy ndarray!")



def manhattan(state, goal):
    distance = 0

    for i in range(1, len(state.ravel())):
        state_coords = np.hstack(np.where(state == i))
        goal_coords = np.hstack(np.where(goal == i))

        distance += np.abs(state_coords - goal_coords).sum() 

    return distance

class Puzzle_Node(object):
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0
    
    def equals(self, other):
        #set_trace()
        return (self.state == other).all()

    def move(self, row_empty, col_empty, row_new, col_new):
        child_state = self.state.copy()
        tmp = self.state[row_new, col_new]
        child_state[row_new, col_new] = 0
        child_state[row_empty,col_empty] = tmp

        return child_state
    
    def generate_children(self):
        children = []
        # Corrodents of the empty block corresponding to row x col
        empty_coord = np.hstack(np.where(self.state == 0))

        # Attempt to move left
        left = empty_coord - [0, 1] 
        if left[1] >= 0:
            #print("move left")
            child_state = self.move(*empty_coord, *left)
            children.append(Puzzle_Node(state=child_state, parent=self))
        # Attempt to move right
        right = empty_coord + [0, 1] 
        if right[1] < self.state.shape[1]:
            #print("move right")
            child_state = self.move(*empty_coord, *right)
            children.append(Puzzle_Node(state=child_state, parent=self))
        ## Attempt to move right
        up = empty_coord - [1, 0] 
        if up[0] >= 0:
            #print("move up")
            child_state = self.move(*empty_coord, *up)
            children.append(Puzzle_Node(state=child_state, parent=self))
        # Attempt to move down
        down = empty_coord + [1, 0] 
        if down[0] < self.state.shape[0]:
            #print("move down")
            child_state = self.move(*empty_coord, *down)
            children.append(Puzzle_Node(state=child_state, parent=self))
        
        return children

class AStar(object):
    def __init__(self, init_state, goal_state):
        self.init = init_state
        self.goal = goal_state
 
    def solve(self):
        open_set = [] # frontier
        closed_set = [] # explored

        # Init state node object
        current_node = Puzzle_Node(state=self.init, parent=None)

        # Init start nodes scores
        current_node.g = 0
        current_node.h = manhattan(self.init, self.goal)
        current_node.f = current_node.g + current_node.h
        current_node.parent = None

        # Add node to open_set
        open_set.append(current_node)
        while open_set:
            # Sort nodes then remove smallest score node adding it to the closed set
            open_set.sort(key= lambda x: x.f, reverse=True)
            current_node = open_set.pop()
            closed_set.append(current_node)
            print("Current f score: {}".format(current_node.f))

            # Goal check
            if current_node.equals(self.goal):
                print("FOUND")
                self.print_solution(current_node)
                print(len(open_set))
                return
            
            # Generate current nodes children
            children = current_node.generate_children() 

            for child in children:
                if any(child.equals(n.state) for n in closed_set):
                    continue
                
                child.g =  current_node.g + 1
                child.h = manhattan(child.state, self.goal)
                child.f = child.g + child.h
                child.parent = current_node

                # Account for child states that already exist in the open_set
                # but are more expensive.
                if any(child.equals(n.state) and child.g > n.g for n in open_set):
                    continue

                # assert consitency of heuristic 
                assert child.h + 1 >= current_node.h
                open_set.append(child)

    def print_solution(self, current_node):
        if current_node.parent is None:
            print(current_node.state)
            print("{} = {} + {}".format(current_node.f, current_node.g, current_node.h))
            return

        self.print_solution(current_node.parent)
        print(current_node.state)
        print("{} = {} + {}".format(current_node.f, current_node.g, current_node.h))
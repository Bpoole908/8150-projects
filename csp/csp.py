import queue
import copy
import random
import time
import functools
from pdb import set_trace

import numpy as np 
from numpy import ma

def bordered(text):
    lines = text.splitlines()
    width = max(len(s) for s in lines)
    res = ['┌' + '─' * width + '┐']
    for s in lines:
        res.append('│' + (s + ' ' * width)[:width] + '│')
    res.append('└' + '─' * width + '┘')

    return '\n'.join(res)

def timeme(func):
    """
        Decoractor for tracking the runtime of a decorated function.

        Args:
            func (function): A Python function.
    """

    @functools.wraps(func)
    def wrapper_time(*args, **kwargs):
        start = time.monotonic()
        output = func(*args, **kwargs)
        total_time = (time.monotonic() - start)
        speed = "Run time of {}: {:.9f} seconds".format(func.__name__, total_time)
        print(bordered(text=speed))

        return output

    return wrapper_time
      
class MapColoring():
    def __init__(self, region, domain_size):
        self.region = region
        self.domain = {s:np.arange(domain_size) for s in region.keys()}

    def check_assignments(self, assigned):
        if assigned is None:
            print("No answer found!")
            return

        for k, c in assigned.items():
            for n in self.region[k]:
                if assigned[n] == c:
                    print("Assignments are NOT consistent!")
        
        self.print_assigned(assigned)
        print("Assignments are consistent!")
        
    def print_assigned(self, assigned):
        [print("{} => {}".format(s, c)) for s, c in assigned.items()]
    @timeme
    def search(self, forward=False, proportion=False, seed=1):
        # np.random.seed(seed)
        random.seed(seed)
        # initial_state = random.choice(self.states_nodes)
        assigned = self.dfs(domain=self.domain)
        self.check_assignments(assigned)
        return assigned
        
    def consistent(self, state, assignments):
        neighbors = self.region[state]        
        for n in neighbors:
            if n in assignments and assignments[n] == assignments[state]:
                return False
        
        return True
    
    def select_unassigned(self, unassigned):
        selected = random.choice(list(unassigned.keys()))

        return selected
            
    # def undo_forward_checking(self, color, changed):
    #         for c in changed:
    #             self.domain[c].mask[color] = False               
                
    def forward_checking(self, color, neighbors, unassigned, domain):
        for n in neighbors:
            if n in unassigned and color in domain[n]:
                color_loc = np.where(domain[n] == color)
                # print(color, domain[n], domain[n][color_loc])
                domain[n] = np.delete(domain[n], color_loc, axis=0)
                if len(domain[n]) == 0:
                    return False, domain

        return True, domain
              
    def dfs(self, domain, assignments={}):
        # [print("{} => {}".format(s, c)) for s, c in assignments.items()]
        if len(assignments) == len(self.region):
            return assignments
        
        # Select unassigned variable
        unassigned = {s:{} for s in self.region.keys() if s not in assignments}
        # [print("\t{}".format(s)) for s in unassigned]
        state = self.select_unassigned(unassigned)
        unassigned.pop(state)

        for color in domain[state]:
            # local_assignments = assignments.copy()
            # local_assignments[state] = color
            assignments[state] = color
            local_domain = domain.copy()
            
            # assert id(assignments) != id(local_assignments)
            inference, local_domain = self.forward_checking(
                color, self.region[state], unassigned, local_domain)
            # print("\n", state, color, inference, self.domain)

            if inference:
                if self.consistent(state, assignments):
                    # return of None means failure
                    assigned = self.dfs(domain=local_domain, assignments=assignments)
                    # Check if a failure occurred
                    if assigned is not None:
                        return assigned
                # If we failed we will reach this point thus undo assignment
            assignments.pop(state)
            # self.undo_forward_checking(color, changed)
        return None
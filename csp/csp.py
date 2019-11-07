import queue
import copy
import random
from pdb import set_trace

import numpy as np 
from numpy import ma
        
class MapColoring():
    def __init__(self, region, domain_size):
        self.region = region
        self.domain = {s:ma.masked_array(np.arange(domain_size)) for s in region.keys()}

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
        
    def search(self, forward=False, proportion=False, seed=1):
        # np.random.seed(seed)
        random.seed(seed)
        # initial_state = random.choice(self.states_nodes)
        assigned = self.dfs()
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
            
    def undo_forward_checking(self, color, changed):
            for c in changed:
                self.domain[c].mask[color] = False               
                
    def forward_checking(self, color, neighbors, unassigned):
        changed = []
        for n in neighbors:
            if n in unassigned: 
                self.domain[n] = ma.masked_where(self.domain[n]==color, self.domain[n])
                changed.append(n)
                if len(self.domain[n].compressed()) == 0:
                    return False, changed

        return True, changed
              
    def dfs(self, assignments={}):
        # [print("{} => {}".format(s, c)) for s, c in assignments.items()]
        if len(assignments) == len(self.region):
            return assignments
        
        # Select unassigned variable
        unassigned = {s:{} for s in self.region.keys() if s not in assignments}
        # [print("\t{}".format(s)) for s in unassigned]
        state = self.select_unassigned(unassigned)
        unassigned.pop(state)

        for color in self.domain[state].compressed():
            # local_assignments = assignments.copy()
            # local_assignments[state] = color
            assignments[state] = color
            
            # assert id(assignments) != id(local_assignments)
            # inference, changed = self.forward_checking(
            #     color, self.region[state], unassigned)
            # print("\n", state, color, inference, self.domain)
            # if inference:
            if self.consistent(state, assignments):
                # return of None means failure
                assigned = self.dfs(assignments)
                # Check if a failure occurred
                if assigned is not None:
                    return assigned
            # If we failed we will reach this point thus undo assignment
            assignments.pop(state)
            # self.undo_forward_checking(color, changed)
            # print(state, color, self.domain, "\n")
        return None
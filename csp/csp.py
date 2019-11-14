import queue
import copy
import random
import time
import functools
from queue import Queue
from pdb import set_trace

import numpy as np 
from numpy import ma

def bordered(text):
    """ Function used to add border around text.
    
        Source: 
           https://bit.ly/353dfGe
    """
    lines = text.splitlines()
    width = max(len(s) for s in lines)
    res = ['┌' + '─' * width + '┐']
    for s in lines:
        res.append('│' + (s + ' ' * width)[:width] + '│')
    res.append('└' + '─' * width + '┘')

    return '\n'.join(res)

def timeme(func):
    """ Decoractor for tracking the runtime of a function.

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

def random_variable(unassigned):
    """ Selects random variables from unassigned variables
    """
    return random.choice(unassigned)

def MRV(unassigned, domain):
    """ Selects variable with the smallest doamin from unassigned variables
    """
    smallest_domain = float('inf')
    
    for u in unassigned:
        u_values = domain[u].compressed()
        if len(u_values) < smallest_domain:
            smallest_var = u
            smallest_domain = len(u_values)

    return smallest_var

def degree_constraint(unassigned, constraints):
    """ Selects variable with the highest number of constraints from unassigned
        variables.
    """
    max_constraint = float('-inf')
    for u in unassigned:
        if len(constraints[u]) > max_constraint:
            max_var = u
            max_constraint = len(constraints[u])
            
    return max_var

def least_constraining_value(state, constraints, domain, unassigned):
    """ Returns domain sorted by most usuable value based on neighboring domains
    
    """
    state_values =  {v:0 for v in domain[state].compressed()}
    neighbors = constraints[state]
    # print(state, domain[state].compressed())
    for n in neighbors:
        if  n != state and n in unassigned:
            neighbors_values = domain[n].compressed()
            for nv in neighbors_values:
                if nv in state_values:
                    state_values[nv] += 1
                    # print("\t", n, nv)

    # sorted(state_values.items(), key=lambda x: x[1]["count"], reverse=True)
    sorted_states = sorted(state_values.items(), key=lambda x:x[1], reverse=True)
    values = [i[0] for i in sorted_states]
    # print(sorted_states)

    return values

class MapColoring():
    def __init__(self, region, domain_size):
        self.region = region
        # self.domain = {np.arange(domain_size) for s in region.keys()}
        self.domain = {s:ma.masked_array(np.arange(domain_size)) for s in region.keys()}
        self.backtracking = 0
        
    @timeme
    def __call__(self, heuristics=False, forward_checking=False, propagation=False, 
                 seed=1, **kwargs):
        random.seed(seed)
            
        assigned = self.dfs(
            forward_checking=forward_checking, propagation=propagation,
            heuristics=heuristics)
        self.check_assignments(assigned)
        
        return assigned
    
    def check_assignments(self, assigned):
        if assigned is None:
            print("No answer found!")
            return

        for k, c in assigned.items():
            for n in self.region[k]:
                if assigned[n] == c:
                    print("ERROR: {} => {} == {} => {}".format(
                        n, assigned[n], k, c))
                    raise ValueError("Assignments are NOT consistent!")
        
        self.print_info(assigned)
        print("Assignments are consistent!")
        
    def print_info(self, assigned):

        for s, c in assigned.items():
            n_colors = {}
            for n in self.region[s]:
                n_colors[n] = assigned[n]
                
            print("{} color: {}".format(s, c)) 
            print("\t Neighboring colors: {}".format(list(n_colors.values())))
        # [print("{} => {}".format(s, c)) for s, c in assigned.items()]
        print("Backtacks: {}".format(self.backtracking))
        
    def consistent_assignments(self, state, assignments):
        neighbors = self.region[state]        
        for n in neighbors:
            if n in assignments and assignments[n] == assignments[state]:
                return False
        
        return True
            
    def undo_mask(self, changed):
        for var, value in changed:
            self.domain[var].mask[value] = False               
                
    def forward_checking(self, state, value, unassigned):
        changed = []
        for n in self.region[state]:
            if n != state and n in unassigned: 
                self.domain[n] = ma.masked_where(self.domain[n]==value, self.domain[n])
                changed.append([n, value])
                if len(self.domain[n].compressed()) == 0:
                    return False, changed
        
        return True, changed
    
    def propagate(self, state, unassigned):
        """ Runs propagation through singleton.
        

        """
        changed = []
        single_valued_domains = Queue()
        for u in unassigned:
            if u != state and len(self.domain[u].compressed()) == 1:
                single_valued_domains.put(u)

        while not single_valued_domains.empty():
            single_state = single_valued_domains.get()
            single_value = self.domain[single_state].compressed()[0] 

            for n in self.region[single_state]:
                # print(n)
                if n!= state and n in unassigned:
                    if single_value in self.domain[n].compressed():
                        # print("\tMASKED")
                        self.domain[n] = ma.masked_where(
                            self.domain[n]==single_value, self.domain[n])
                        changed.append([n, single_value])
                        
                        if len(self.domain[n].compressed()) == 1:
                            # print("\tQUEUED")
                            single_valued_domains.put(n) 
                        elif len(self.domain[n].compressed()) == 0:
                            return False, changed
                    
        return True, changed
            
    def dfs(self, assignments={}, heuristics=False, forward_checking=False, propagation=False):
        """ Run depth first search regarding CSP.

            Uses recursive DFS to inherently allow for backtracking.
            
            Args:
                assignments (dict): Holds variable to color mapping.
                
                heuristics (bool): If true enables all heuristics for initial
                    variable, variable, and value selection.
                
                forward_checking (bool): Enables forward checking for CSP.
                
                propagation (bool): Enables propagation through singletons for
                    CSP.
                    
            Returns:
                Returns None indicating backtracking is needed or problem is 
                unsolvable.
        """
        # Check if all assignments have been made
        if len(assignments) == len(self.region):
            return assignments

        # Select unassigned variable
        unassigned = [s for s in self.region.keys() if s not in assignments]

        # Select variable
        if heuristics:
            if len(assignments) == 0:
                # Initialize with state which has most constraints
                state = degree_constraint(unassigned, self.region)
                print("Initial State: {}".format(state))
            else:
                # Follow MRV
                state = MRV(unassigned, self.domain)
        elif len(assignments) == 0:
            # Initialize with random state
            state = random_variable(unassigned)
            print("Initial State: {}".format(state))
        else:
            # Follow static path of states
           state = unassigned[0] 
            
        # Select values
        if heuristics:
            domain = least_constraining_value(state, self.region, 
                                              self.domain, unassigned)
        else:
            domain = self.domain[state].compressed()
            
        for value in domain:
            assignments[state] = value

            # Preform forward checking if enabled
            if forward_checking:
                forward, forward_changed = self.forward_checking(
                    state, value, unassigned)
            else:
                forward = True
            
            # Preform propgation through singletons if enabled
            if propagation:
                # print(assignments)
                prop, prop_changed = self.propagate(state, unassigned)
            else:
                prop = True
                
            # Check if forward and prop were successful
            if forward and prop:
                # Check consistency
                if self.consistent_assignments(state, assignments):
                    # return of None means failure
                    assigned = self.dfs(assignments, heuristics, 
                                        forward_checking, propagation)
                    # Check if a failure occurred
                    if assigned is not None:
                        return assigned
            # Now backtrack undoing previous assignment, forward and propagation
            assignments.pop(state)
            if forward_checking: self.undo_mask(forward_changed)
            if propagation: self.undo_mask(prop_changed)
            self.backtracking += 1
        return None
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
    """ Decorator for tracking the runtime of a function.

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
    
        Args:
            unassigned (iterable): Any iterable object that contains names of
                values in constraints.
    """
    return random.choice(unassigned)

def MRV(unassigned, domain):
    """ Selects variable with the smallest domain from unassigned variables
    
        Args:
            domain (dict): Dictionary where nodes act as keys mapped to potential
                values.
                
            unassigned (iterable): Any iterable object that contains names of
                values in constraints.
    """
    smallest_domain = float('inf')
    
    for u in unassigned:
        u_domain = domain[u]
        if len(u_domain) < smallest_domain:
            smallest_var = u
            smallest_domain = len(u_domain)

    return smallest_var

def degree_constraint(constraints, unassigned):
    """ Selects variable with the highest number of constraints from unassigned
        variables.
        
        Args:
            constraints (dict): Dictionary of constraints are nodes are keys
                which are mapped to their constraints. 
                
            unassigned (iterable): Any iterable object that contains names of
                values in constraints.
    """
    max_constraint = float('-inf')
    for u in unassigned:
        if len(constraints[u]) > max_constraint:
            max_var = u
            max_constraint = len(constraints[u])
            
    return max_var

def least_constraining_value(state, constraints, unassigned, domain):
    """ Returns domain sorted by most usable value based on neighboring domains

        Args:
            constraints (dict): Dictionary of constraints are nodes are keys
                which are mapped to their constraints. 
                
            unassigned (iterable): Any iterable object that contains names of
                values in constraints.

            domain (dict): Dictionary where nodes act as keys mapped to potential
                values.
    """
    state_values =  {v:0 for v in domain[state]}
    neighbors = constraints[state]
    
    for n in neighbors:
        if n != state and n in unassigned:
            neighbor_domain = domain[n] 
            for nv in neighbor_domain:
                if nv in state_values:
                    state_values[nv] += 1

    sorted_states = sorted(state_values.items(), key=lambda x:x[1], reverse=True)
    values = [i[0] for i in sorted_states]

    return values

class MapColoring():
    def __init__(self, region, domain_size):
        self.region = region
        self.domain = {s:np.arange(domain_size) for s in region.keys()}
        self.backtracking = 0
        
    @timeme
    def __call__(self, heuristics=False, forward_checking=False, propagation=False, 
                 seed=1, **kwargs):
        random.seed(seed)
            
        assigned = self.dfs(
            domain=self.domain, forward_checking=forward_checking, 
            propagation=propagation, heuristics=heuristics)
        self.check_assignments(assigned)
        
        return assigned
    
    def check_assignments(self, assigned):
        """ Checks final color assignments are actually consistent.
            
            Args:
                assigned: Dictionary where states that have been 
                    assigned a color act as keys and the actual color assigned
                    is the value.
        """ 
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
        """ Prints final color assignments and checks if assignments are actually
            consistent.
            
            Args:
                assigned: Dictionary where states that have been 
                    assigned a color act as keys and the actual color assigned
                    is the value.
        """ 

        for s, c in assigned.items():
            n_colors = {}
            for n in self.region[s]:
                n_colors[n] = assigned[n]
                
            print("{} color: {}".format(s, c)) 
            print("\t Neighboring colors: {}".format(list(n_colors.values())))

        print("Backtacks: {}".format(self.backtracking))
        
    def consistent(self, state, assignments):
        """ Checks for consistency in an color assignment. 

            Args:
                state (string): Name of current state.
                
                assignments (dict): Dictionary where states that have been 
                    assigned a color act as keys and the actual color assigned
                    is the value.
            
            Returns:
                Returns a boolean where True indicates assignment maintains
                consitency.
        """
        neighbors = self.region[state]        
        for n in neighbors:
            if n in assignments and assignments[n] == assignments[state]:
                return False
        
        return True

    def forward_checking(self, color, neighbors, unassigned, domain):
        """ Eliminates colors from neighbors when a color is selected for a given
            state.
        
            Args:
                color (int): Color selected by current state to assign to itself.
                
                neighbors (list): Neighbors of current state
                
                unassigned (iterable): Any iterable object that contains names of
                    values in constraints.
                
                domain (dict): Dictionary where states act as keys mapped to 
                    potential remaining colors in their domain.
            
            Return:
                Returns True if colors in neighboring domains can be eliminated
                without producing an empty domain. Also, returns updated domain.
        """
        for n in neighbors:
            if n in unassigned and color in domain[n]:
                color_loc = np.where(domain[n] == color)
                domain[n] = np.delete(domain[n], color_loc, axis=0)
                if len(domain[n]) == 0:
                    return False, domain

        return True, domain
    
    def propagate(self, unassigned, domain):
        """ Eliminates colors from neighbors if a state with a single color is 
            detected.
        
            Args:
                unassigned (iterable): Any iterable object that contains names of
                    values in constraints.
                
                domain (dict): Dictionary where states act as keys mapped to 
                    potential remaining colors in their domain.
        """
        changed = []
        single_valued_domains = Queue()
        
        # Load any states with a single color in their domain
        for u in unassigned:
            if len(domain[u]) == 1:
                single_valued_domains.put(u)

        # Loop through single valued domain states adding more as you go (if needed).
        while not single_valued_domains.empty():
            single_state = single_valued_domains.get()
            single_color= domain[single_state][0]
            
            for n in self.region[single_state]:
                if n in unassigned:
                    if single_color in domain[n]:
                        color_loc = np.where(domain[n] == single_color)
                        domain[n] = np.delete(domain[n], color_loc, axis=0)
                        if len(domain[n]) == 1: 
                            single_valued_domains.put(n) 
                        elif len(domain[n]) == 0: 
                            return False, domain
                    
        return True, domain
            
    def dfs(self, domain, assignments={}, heuristics=False, 
            forward_checking=False, propagation=False):
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

        # Find all unassigned variable
        unassigned = {s:{} for s in self.region.keys() if s not in assignments}

        # Select state (variable) either using heuristics or randomly otherwise.
        if heuristics:
            if len(assignments) == 0:
                # Initialize with state which has most constraints
                state = degree_constraint(unassigned=unassigned.keys(), 
                                          constraints=self.region)
                print("Initial State: {}".format(state))
            else:
                # Follow MRV
                state = MRV(unassigned=unassigned.keys(), domain=domain)
        else:
            # Initialize with random state
            state = random_variable(unassigned=list(unassigned.keys()))
            if len(assignments) == 0:
                print("Initial State: {}".format(state))
               
        # Remove selected state from unassigned
        # we can do this because in this local instance this is the only state
        # we select. Therefore, this does no effect any other recursion instance.
        unassigned.pop(state)
        
        # Select values either based on heuristic or given order.
        if heuristics:
            colors = least_constraining_value(state=state, 
                                              constraints=self.region, 
                                              unassigned=unassigned.keys(),
                                              domain=domain)
        else:
            colors = domain[state]
            
        for color in colors:
            assignments[state] = color # Assign color we want to try
            
             # Copy domain instead of tracking changes
            local_domain = domain.copy() if forward_checking or propagation else domain

            if forward_checking:
                forward, local_domain = self.forward_checking(
                    color=color, neighbors=self.region[state], 
                    unassigned=unassigned.keys(), domain=local_domain)
            else:
                forward = True
 
            if propagation:
                prop, local_domain = self.propagate(unassigned=unassigned.keys(), 
                                                    domain=local_domain)
            else:
                prop = True  
                
            # Check if forward and prop were successful
            if forward and prop:
                # Check consistency
                if self.consistent(state=state, assignments=assignments):
                    # return of None means failure
                    assigned = self.dfs(domain=local_domain, 
                                        assignments=assignments, 
                                        heuristics=heuristics, 
                                        forward_checking=forward_checking, 
                                        propagation=propagation)
                    # Check if a failure occurred
                    if assigned is not None:
                        return assigned
                    
            # Now backtrack undoing previous color
            # At this point we are inherently forgetting any forward or 
            # propgations due to the nature of local copies of the domain.
            self.backtracking += 1
            assignments.pop(state)
            
        return None
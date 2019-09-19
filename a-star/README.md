# 8-Puzzle Problem via A* Report

## Summary
### Problem

The 8-puzzel problem entails a 3x3 grid in which the numbers 0-8 are randomly shuffled within said grid. The goal is to get from some, typically random, initial state to some goal state. To do so the agent or player must move then 0 tile around (up, left, right, or down depending on its position). Every time the 0 tile is moved it switches place with the tile it’s moving to. The goal is to get to the goal state in as few steps as possible.

There are some cases when it is impossible for the initial state to ever reach the goal state. This can be tested for my checking the number of inversions the initial state has (with the goal state acting as the number system). Depending on implementation this usually causes a infinite loop as there are infinitely many $$f(n)$$ scores with the same value (local minimum), hence this is the only condition that makes $$A^*$$ incomplete.


## Program Structure

### Running The Program
To run the program via command line simply run `python .`   or `python __main__.py` .

Configure Initial and Goal States
To set the initial and goal state open the `config.yml` file and edit matrix representations within this file. The variable `init_state` corresponds to the initial state and the variable `goal_state` corresponds to the goal state. If you wish to change the heuristic you can change the `heuristic` variable to "manhattan” or 
“miss_placed.”

### __main__.py
The `__main__.py`  file is in charge of loading the config file, checking if the given initial and goals states are valid, checking if the problem is solvable, and running A^*. If you want to change the initial or goal state then you can do so by editing the `config.yml` (see section Configure Initial and Goal States). One function of note is the `solvable()`  function which will let you know if the initial state is actually solvable. If the initial state is not solvable then you will be warned that proceeding will cause an infinite loop (if you still wish to continue enter “c” into the command prompt). The other functions of note are the heuristic functions `manhattan()` and `miss_placed().`  The `manhattan()` is in charge of calculating the Manhattan distance of an entire state to a given goal. The `miss_placed()` simply counts the number of tiles/numbers that are out of place in comparison to the goal (the max heuristic is then 9). It should be noted that `miss_placed()` can take an extremely long time to solve harder problems (I do not recommend using it).

### a_star.py
The `a_star.py`  file contains the `AStar`  and `PuzzleNode`  classes. The `AStar` class is in charge of running the $$A^*$$ algorithm. Once again, if the problem is not solvable the $$A^*$$ algorithm will infinitely loop. If a solution is found then it will recursively print the solution to the command line along with the nodes explored and generated. The `PuzzleNode` class is in charge of tracking each state representation, the parent, f, g, and h scores. All the move decisions and children are generated via this class as well. 

### requirements.txt
The requirements file contains all the required packages to run my code. The following command for pip should suffice (a Conda install should also work). 


    `$ pip install -r requirements.txt`
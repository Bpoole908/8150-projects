
# 8-Puzzle Problem via A* Report

## Summary

### Problem

The 8-puzzel problem entails a 3x3 grid in which the numbers 0 to $n$ are randomly shuffled within said grid. The goal is to get from some, typically random, initial state to some given goal state. To do so the agent or player must move then 0 tile around (up, left, right, or down depending on its position). Every time the 0 tile is moved it switches places with the tile in the position it is moving to. The goal is to match the goal state in as few steps as possible.

There are some cases when it is impossible for the initial state to reach the goal state. This can be tested for my checking the number of inversions the initial state has (with the goal state acting as the number system). Depending on implementation this usually causes a long search through the entire state space or an infinite loop if repeated states are not considered.

## Program Structure

### Running The Program

To run the program via command line simply path to the `a-star/` directory and run `python .` or `python __main__.py` .

### Configure Initial and Goal States
To set the initial and goal state open the `config.yml` file and edit the matrix representations within this file. The variable `init_state` corresponds to the initial state and the variable `goal_state` corresponds to the goal state. If you wish to change the heuristic you can change the `heuristic` variable to "manhattan” or “misplaced.”

### __main__.py

The `__main__.py` file is in charge of loading the config file, checking if the given initial and goals states are valid, checking if the problem is solvable, and running $A^*$. If you want to change the initial or goal state then you can do so by editing the `config.yml` (see section Configure Initial and Goal States). One function of note is the `solvable()` function which will let you know if the initial state is actually solvable. If the initial state is not solvable then you will be warned that proceeding will cause the algorithm to search the entire state space (if you still wish to continue enter “c” into the command prompt). The other functions of note are the heuristic functions `manhattan()` and `misplaced().` The `manhattan()` is in charge of calculating the Manhattan distance of an entire state to a given goal. The `misplaced()` simply counts the number of tiles/numbers that are out of place in comparison to the goal (the max heuristic is then 9 for 3x3 when the 0 tile is included). It should be noted that `mispalced()` can take an extremely long time to solve harder problems (I do not recommend using it).

### a_star.py

The `a_star.py` file contains the `AStar` and `PuzzleNode` classes. The `AStar` class is in charge of running the  $A^*$ algorithm. Once again, if the problem is not solvable the $A^*$ algorithm will loop through the entire state space and return false. If a solution is found then it will recursively print the solution to the command line along with the nodes explored and generated and finally return true. The `PuzzleNode` class is in charge of tracking each state representation, the parent, f, g, and h scores. All the move decisions and children are generated via the `PuzzleNode` class as well.

### requirements.txt

The requirements file contains all the required packages to run my code. The following command for pip should suffice (a Conda install should work as well).

`pip install -r requirements.txt`

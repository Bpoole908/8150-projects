# N-Queen Report

# Problem
----------

The N-Queen problem consists of a square board $$(n,n)$$ where you are given $$n$$ queens to place on the board. The goal is to place each queen in a way such that no queen is “attacking” another queen. Attacking in this instances means another queen can not be in the same row, column, or diagonal as any other queen. 

The N-queens problem is a NP-hard problem; therefore, having no solution in polynomial time. However, we can began to find good solutions using naive optimization methods such as hill-climbing.

## Goal

The goal is to place the queens on the board such that no queen is attacking another queen, i.e. another queen can not be in the same row, column, or diagonal as any other queen.

## Constraints and Code Caveats

The first constraint to my N-queens task is inherit to the task rules. That is, no queen can be in the same row, column, or diagonal as any other queen. The second constraint is that, typically, each queen is constrained to a column or a row when initializing the board to further simplify the problem. In my code all queens are restricted to a unique row.

# Algorithms
----------
## Basic Hill Climbing

The basic hill climbing search method simply looks for the minimum value (or maximum depending on the type of optimization problem) and moves in said direction. This means, the algorithm is always following a path of decent or ascent. The hill climbing algorithm will either find a solution (in our case no conflicts) or will terminate because the heuristic (number of conflicts) has increased or is equal to the previous value.

## Hill Climbing with Sideways Moves

To improve upon the basic hill climbing algorithm sideways moves can be introduced. Any optimization problem can become trapped in a flat plan located on the optimization function called a saddle point. That is, all moves are equal (the local plane is flat). One way to over comes this is to allow for what are called sideways moves. This means that we continuously and randomly pick among the  equally minimal moves, instead of terminating, until the agent finds its way out of the saddle point or some threshold number of sideways moves is reached. If the threshold number of sideways moves is reached then the search can be terminated.


## Hill Climbing with Random Restarts

Improving upon sideways moves further is random restarts. Random restarts randomly reinitializes the board when the basic climbing or sideways move algorithms become stuck (when they would normally terminate). This will keep occurring until a solution is found,  practically guaranteeing a solution with a probability of or near 1.


## Heuristic (Queen Conflicts)

The most common heuristic is to count there total number of attacking moves being made by all the queens on the board (where attacking order doesn't matter).  To optimize given this heuristic we want to move the queen that creates the least amount of conflicts, repeating this until a solution is found. In case there are multiple moves with minimum number of conflicts then a random choice from among them will suffice. If no solution is found, given a saddle point has been found, then we can restart the problem, take sideways moves, or end the search with no solution.


![Here we can see 3 conflicts all which are due to queens being in same column](https://paper-attachments.dropbox.com/s_991821443821FA4D7236A58F57043A78F86BFA34308065FB392EA87476FE8D89_1571330728469_image.png)
![Here we can see there are now no conflicting queens](https://paper-attachments.dropbox.com/s_991821443821FA4D7236A58F57043A78F86BFA34308065FB392EA87476FE8D89_1571330904041_image.png)

# Program Structure
----------
## Running  Code

To run the program via command line simply path to the `8-queens/` directory and run `python .` or `python __main__.py` .

## Installing Requirements

The requirements file `requirements.txt` contains all the required packages to run my code. The following command for pip should suffice (a Conda install should work as well).

`pip install -r requirements.txt`

## Configuration

To set the number queens, algorithm type, epochs, and sideways moves open the `config.yml` file and change their respective parameters based on the template given below.

| Parameters       | Definition                                                                                                                                                                                                          |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `n`              | This is the number of queens to generate (doubles as board size$$(n, n)$$.                                                                                                                                          |
| `seed`           | Seed is used when INITIALLY generating board, i.e. epoch is set to 1. This allows for deterministic qualities for testing and can be disable by entering `Null`. Seed will not effect epochs after 1.               |
| `htype`          | Used to select the hill climbing algorithm. Your choice of inputs are “basic”, “sideways”, or “random-restarts”. Any other inputs will throw an exception.                                                          |
| `epochs`         | Used to determine the number of tests that should be ran. If you want to see a single instance of an algorithm enter 1.                                                                                             |
| `sideways_moves` | Used to determine the number of sideways moves applied to <br>`HillClimbing.sideways_moves` and  `HillClimbing.random_restarts` **ONLY.** If given but `HillClimbing.basic` is used then this parameter is ignored. |

## main.py

The `__main__.py` file is in charge of loading the config file and running the passed algorithms set number of times in order to calculate averages. Each algorithm has a corresponding wrapper `basic_stats`, `sideways_moves_stats`, and `random_restarts_stats`. Each wrapper will produce a set of averages based on a passed number of epochs. Every epoch represents a new N-queens problem with a new initialization. If you do not wish to run an algorithm many times in a row simply set epochs equal to one in the config `epochs: 1`. See the configuration section above for changing algorithms and setting other parameters.


## queens.py

The `queens.py` file contains the `Queens` class and a utility function for adding a boarder to test called `boarder`. The `Queens` class is in charge of the N-queens problem which means maintaining the board, generating neighbors and calculating the number of conflicts. See the chart below for details on each method. Side note, any time the “current board” is mentioned this is referring to the current state of `self.board`.

| **Method**        | **Description**                                                                                                                                        |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `populate_board`  | Populates a $$(n, n)$$ board given a random seed.                                                                                                      |
| `print_board`     | Prints the board in a clean but slower fashion. Allows for you to specify what symbols should be used for empty spaces and queens.                     |
| `coords_to_board` | Translates all passed queen coordinates to board form. Meaning, create a new board from a set of coordinates that specifics where to place the queens. |
| `get_coords`      | Gets all coordinates (row, col) for queens on the current board.                                                                                       |
| `queen_conflicts` | Check a single queen's conflicts given all other queen’s coordinates.                                                                                  |
| `heuristic`       | Calculates total number of conflicts given the queens coordinates or from the current board.                                                           |
| `neighbors`       | Generates all neighbors from the current board state.                                                                                                  |

## hill_climbing.py

The `hill_climbing.py` file contains all the code for each hill climbing algorithm. All algorithms are found in `HillClimbing` class which acts as a grouping mechanism for said algorithms.  This means all methods inside `HillClimbing` are static.

| **Method**        | **Description**                                                                                                                                                                                                                                                                                             |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `basic`           | implements the basic hill climbing algorithm that terminates when the heuristic increases or is equal to the previous state. This algorithm will randomly select from equally minimal neighbors when deciding on which action to take.                                                                      |
| `sideways_moves`  | Implements the sideways moves hill climbing algorithm that terminates when the sideways moves threshold is exceeded.  This algorithm will also randomly select from equally minimal neighbors. Setting the `threshold` parameter  to 1 is the same as running the `basic` method.                           |
| `random_restarts` | Implements random restart hill climbing algorithm that restarts at random initializes when no solution could previously be found.  By default this algorithm uses sideways moves but can be disabled by setting `threshold` to 1.  This algorithm will also randomly select from equally minimal neighbors. |



# Basic Hill Climbing Results
----------
| **Runs**                  | 100  |
| ------------------------- | ---- |
| **N Queens**              | 8    |
| **Average Success Rate**  | .14  |
| **Average Success Steps** | 3.71 |
| **Average Failure Rate**  | .86  |
| **Average Failure Steps** | 3.99 |



## Success 1
    ┌────────────────┐
    │0 0 0 Q 0 0 0 0 │
    │0 0 0 Q 0 0 0 0 │
    │0 0 0 0 Q 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    │0 0 0 0 0 0 0 Q │
    │0 0 0 0 0 0 Q 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 Q 0 0 0 │
    └────────────────┘
    conflicts: 11
    ┌────────────────┐
    │0 0 0 Q 0 0 0 0 │
    │0 0 0 Q 0 0 0 0 │
    │0 0 0 0 Q 0 0 0 │
    │0 0 Q 0 0 0 0 0 │
    │0 0 0 0 0 0 0 Q │
    │0 0 0 0 0 0 Q 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 Q 0 0 0 │
    └────────────────┘
    conflicts: 8
    step: 1
    ┌────────────────┐
    │0 0 0 Q 0 0 0 0 │
    │0 0 0 Q 0 0 0 0 │
    │0 0 0 0 Q 0 0 0 │
    │0 0 Q 0 0 0 0 0 │
    │0 0 0 0 0 0 0 Q │
    │0 0 0 0 0 0 Q 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 0 Q 0 0 │
    └────────────────┘
    conflicts: 5
    step: 2
    ┌────────────────┐
    │0 0 0 Q 0 0 0 0 │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 0 Q 0 0 0 │
    │0 0 Q 0 0 0 0 0 │
    │0 0 0 0 0 0 0 Q │
    │0 0 0 0 0 0 Q 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 0 Q 0 0 │
    └────────────────┘
    conflicts: 3
    step: 3
    ┌────────────────┐
    │0 0 0 Q 0 0 0 0 │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 0 Q 0 0 0 │
    │0 0 Q 0 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 0 Q 0 0 │
    └────────────────┘
    conflicts: 2
    step: 4
    ┌────────────────┐
    │0 0 0 Q 0 0 0 0 │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 0 Q 0 0 0 │
    │0 0 Q 0 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 0 0 Q 0 0 │
    └────────────────┘
    conflicts: 1
    step: 5
    ┌────────────────┐
    │0 0 0 Q 0 0 0 0 │
    │0 0 0 0 0 0 0 Q │
    │0 0 0 0 Q 0 0 0 │
    │0 0 Q 0 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 0 0 Q 0 0 │
    └────────────────┘
    conflicts: 0
    step: 6
    SUCCESS!
    
## Success 2
    ┌────────────────┐
    │0 Q 0 0 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 Q 0 0 0 │
    │0 Q 0 0 0 0 0 0 │
    │0 0 Q 0 0 0 0 0 │
    │0 Q 0 0 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 Q 0 0 0 0 │
    └────────────────┘
    conflicts: 13
    ┌────────────────┐
    │0 Q 0 0 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 Q 0 0 0 │
    │0 Q 0 0 0 0 0 0 │
    │0 0 Q 0 0 0 0 0 │
    │0 0 Q 0 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 Q 0 0 0 0 │
    └────────────────┘
    conflicts: 8
    step: 1
    ┌────────────────┐
    │0 Q 0 0 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 Q 0 0 0 │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 0 0 0 0 Q │
    │0 0 Q 0 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 Q 0 0 0 0 │
    └────────────────┘
    conflicts: 4
    step: 2
    ┌────────────────┐
    │0 Q 0 0 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 Q 0 0 0 │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 0 0 0 0 Q │
    │0 0 Q 0 0 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    │0 0 0 Q 0 0 0 0 │
    └────────────────┘
    conflicts: 2
    step: 3
    ┌────────────────┐
    │0 0 0 0 0 Q 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 Q 0 0 0 │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 0 0 0 0 Q │
    │0 0 Q 0 0 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    │0 0 0 Q 0 0 0 0 │
    └────────────────┘
    conflicts: 0
    step: 4
    SUCCESS!
## Failure 1
    ┌────────────────┐
    │0 Q 0 0 0 0 0 0 │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 0 0 Q 0 0 │
    │0 0 0 Q 0 0 0 0 │
    │0 0 0 Q 0 0 0 0 │
    │0 0 0 0 0 0 0 Q │
    │0 0 0 0 Q 0 0 0 │
    │0 0 0 0 Q 0 0 0 │
    └────────────────┘
    conflicts: 5
    ┌────────────────┐
    │0 Q 0 0 0 0 0 0 │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 0 0 Q 0 0 │
    │0 0 0 Q 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 0 0 0 Q │
    │0 0 0 0 Q 0 0 0 │
    │0 0 0 0 Q 0 0 0 │
    └────────────────┘
    conflicts: 3
    step: 1
    ┌────────────────┐
    │0 Q 0 0 0 0 0 0 │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 0 0 Q 0 0 │
    │0 0 0 Q 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 0 0 0 Q │
    │0 0 0 0 Q 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    └────────────────┘
    conflicts: 2
    step: 2
    ┌────────────────┐
    │0 Q 0 0 0 0 0 0 │
    │0 0 Q 0 0 0 0 0 │
    │0 0 0 0 0 Q 0 0 │
    │0 0 0 Q 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 0 0 0 Q │
    │0 0 0 0 Q 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    └────────────────┘
    conflicts: 1
    step: 3
    ┌────────────────┐
    │0 0 0 0 0 Q 0 0 │
    │0 0 Q 0 0 0 0 0 │
    │0 0 0 0 0 Q 0 0 │
    │0 0 0 Q 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 0 0 0 Q │
    │0 0 0 0 Q 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    └────────────────┘
    conflicts: 1
    step: 4
    FAILED!


## Failure 2
    ┌────────────────┐
    │0 0 Q 0 0 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    │0 0 0 0 0 0 0 Q │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 0 0 Q 0 0 │
    │0 0 0 0 0 0 Q 0 │
    │0 0 0 0 0 0 0 Q │
    │0 0 Q 0 0 0 0 0 │
    └────────────────┘
    conflicts: 10
    ┌────────────────┐
    │0 0 Q 0 0 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    │0 0 0 0 0 0 0 Q │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 0 Q 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    │0 0 0 0 0 0 0 Q │
    │0 0 Q 0 0 0 0 0 │
    └────────────────┘
    conflicts: 6
    step: 1
    ┌────────────────┐
    │0 0 Q 0 0 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    │0 0 0 0 0 0 0 Q │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 0 Q 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 Q 0 0 0 0 0 │
    └────────────────┘
    conflicts: 4
    step: 2
    ┌────────────────┐
    │0 0 Q 0 0 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    │0 0 0 0 0 0 0 Q │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 0 Q 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 Q 0 0 0 0 │
    └────────────────┘
    conflicts: 2
    step: 3
    ┌────────────────┐
    │0 0 Q 0 0 0 0 0 │
    │0 0 0 0 Q 0 0 0 │
    │0 0 0 0 0 0 0 Q │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 0 Q 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 Q 0 0 0 0 │
    └────────────────┘
    conflicts: 1
    step: 4
    ┌────────────────┐
    │0 0 Q 0 0 0 0 0 │
    │0 0 0 0 0 Q 0 0 │
    │0 0 0 0 0 0 0 Q │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 0 Q 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 Q 0 0 0 0 │
    └────────────────┘
    conflicts: 1
    step: 5
    FAILED!
# Sideways Steps Hill Climbing Results
----------
| **Runs**                  | 100   |
| ------------------------- | ----- |
| **N Queens**              | 8     |
| **Sideways Moves**        | 100   |
| **Average Success Rate**  | .96   |
| **Average Success Steps** | 16.20 |
| **Average Failure Rate**  | .04   |
| **Average Failure Steps** | 53.75 |

## Success 1
    ┌────────────────┐
    │0 0 0 0 0 0 0 Q │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 Q 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    │0 Q 0 0 0 0 0 0 │
    │0 0 Q 0 0 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    └────────────────┘
    conflicts: 3
    ┌────────────────┐
    │0 0 0 0 0 0 0 Q │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 Q 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    │0 0 0 0 Q 0 0 0 │
    │0 0 Q 0 0 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    └────────────────┘
    conflicts: 2
    step: 1
    sideways move: 0
    ┌────────────────┐
    │0 0 0 0 0 0 0 Q │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 Q 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    │0 0 0 0 Q 0 0 0 │
    │0 0 Q 0 0 0 0 0 │
    │0 0 0 0 0 Q 0 0 │
    └────────────────┘
    conflicts: 0
    step: 2
    sideways move: 0
    SUCCESS!
## Success 2
    ┌────────────────┐
    │0 0 0 0 0 Q 0 0 │
    │0 Q 0 0 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 0 Q 0 0 │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    │0 0 0 0 0 0 0 Q │
    └────────────────┘
    conflicts: 7
    ┌────────────────┐
    │0 0 0 0 0 Q 0 0 │
    │0 0 0 Q 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 0 Q 0 0 │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    │0 0 0 0 0 0 0 Q │
    └────────────────┘
    conflicts: 3
    step: 1
    sideways move: 0
    ┌────────────────┐
    │0 0 0 0 0 Q 0 0 │
    │0 0 0 Q 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 Q 0 0 0 0 │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    │0 0 0 0 0 0 0 Q │
    └────────────────┘
    conflicts: 3
    step: 2
    sideways move: 1
    ┌────────────────┐
    │0 0 0 0 0 Q 0 0 │
    │0 0 0 Q 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 Q 0 0 0 0 │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    │0 0 Q 0 0 0 0 0 │
    └────────────────┘
    conflicts: 2
    step: 3
    sideways move: 0
    ┌────────────────┐
    │0 0 0 0 0 Q 0 0 │
    │0 0 0 0 0 0 0 Q │
    │Q 0 0 0 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 Q 0 0 0 0 │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    │0 0 Q 0 0 0 0 0 │
    └────────────────┘
    conflicts: 1
    step: 4
    sideways move: 0
    ┌────────────────┐
    │0 0 0 0 0 Q 0 0 │
    │0 0 0 0 0 0 0 Q │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 Q 0 0 0 │
    │0 0 0 Q 0 0 0 0 │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    │0 0 Q 0 0 0 0 0 │
    └────────────────┘
    conflicts: 1
    step: 5
    sideways move: 1
    ┌────────────────┐
    │0 0 0 0 0 Q 0 0 │
    │0 0 0 0 0 0 0 Q │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 Q 0 0 0 │
    │0 0 0 0 0 0 0 Q │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    │0 0 Q 0 0 0 0 0 │
    └────────────────┘
    conflicts: 1
    step: 6
    sideways move: 2
    ┌────────────────┐
    │0 0 0 0 0 Q 0 0 │
    │0 0 0 Q 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 Q 0 0 0 │
    │0 0 0 0 0 0 0 Q │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    │0 0 Q 0 0 0 0 0 │
    └────────────────┘
    conflicts: 0
    step: 7
    sideways move: 0
    SUCCESS!
## Failure 1: Increase in score
    ┌────────────────┐
    │0 0 0 Q 0 0 0 0 │
    │0 0 Q 0 0 0 0 0 │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 Q 0 0 0 0 │
    │0 0 0 Q 0 0 0 0 │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 0 0 0 0 Q │
    │0 Q 0 0 0 0 0 0 │
    └────────────────┘
    conflicts: 12
    ┌────────────────┐
    │0 0 0 Q 0 0 0 0 │
    │0 0 Q 0 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 Q 0 0 0 0 │
    │0 0 0 Q 0 0 0 0 │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 0 0 0 0 Q │
    │0 Q 0 0 0 0 0 0 │
    └────────────────┘
    conflicts: 7
    step: 1
    sideways move: 0
    ┌────────────────┐
    │0 0 0 0 Q 0 0 0 │
    │0 0 Q 0 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 Q 0 0 0 0 │
    │0 0 0 Q 0 0 0 0 │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 0 0 0 0 Q │
    │0 Q 0 0 0 0 0 0 │
    └────────────────┘
    conflicts: 4
    step: 2
    sideways move: 0
    ┌────────────────┐
    │0 0 0 0 Q 0 0 0 │
    │0 0 Q 0 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    │0 0 0 Q 0 0 0 0 │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 0 0 0 0 Q │
    │0 Q 0 0 0 0 0 0 │
    └────────────────┘
    conflicts: 2
    step: 3
    sideways move: 0
    ┌────────────────┐
    │0 0 0 0 Q 0 0 0 │
    │0 0 Q 0 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    │0 0 0 Q 0 0 0 0 │
    │0 0 0 0 0 Q 0 0 │
    │0 0 0 0 0 0 0 Q │
    │0 Q 0 0 0 0 0 0 │
    └────────────────┘
    conflicts: 1
    step: 4
    sideways move: 0
    ┌────────────────┐
    │0 0 0 0 Q 0 0 0 │
    │0 0 0 0 Q 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    │0 0 0 Q 0 0 0 0 │
    │0 0 0 0 0 Q 0 0 │
    │0 0 0 0 0 0 0 Q │
    │0 Q 0 0 0 0 0 0 │
    └────────────────┘
    conflicts: 2
    step: 5
    sideways move: 0
    FAILED!
## Failure 2: Increase in score
    ┌────────────────┐
    │0 0 Q 0 0 0 0 0 │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 Q 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 Q 0 0 0 │
    │0 Q 0 0 0 0 0 0 │
    │0 Q 0 0 0 0 0 0 │
    │0 Q 0 0 0 0 0 0 │
    └────────────────┘
    conflicts: 9
    ┌────────────────┐
    │0 0 Q 0 0 0 0 0 │
    │0 0 0 0 0 Q 0 0 │
    │0 0 0 Q 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 Q 0 0 0 │
    │0 Q 0 0 0 0 0 0 │
    │0 Q 0 0 0 0 0 0 │
    │0 Q 0 0 0 0 0 0 │
    └────────────────┘
    conflicts: 5
    step: 1
    sideways move: 0
    ┌────────────────┐
    │0 0 Q 0 0 0 0 0 │
    │0 0 0 0 0 Q 0 0 │
    │0 0 0 Q 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 Q 0 0 0 │
    │0 Q 0 0 0 0 0 0 │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    └────────────────┘
    conflicts: 2
    step: 2
    sideways move: 0
    ┌────────────────┐
    │0 0 Q 0 0 0 0 0 │
    │0 0 0 0 0 Q 0 0 │
    │0 0 0 Q 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 Q 0 0 0 │
    │0 0 0 0 0 0 0 Q │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    └────────────────┘
    conflicts: 1
    step: 3
    sideways move: 0
    ┌────────────────┐
    │0 0 0 Q 0 0 0 0 │
    │0 0 0 0 0 Q 0 0 │
    │0 0 0 Q 0 0 0 0 │
    │Q 0 0 0 0 0 0 0 │
    │0 0 0 0 Q 0 0 0 │
    │0 0 0 0 0 0 0 Q │
    │0 Q 0 0 0 0 0 0 │
    │0 0 0 0 0 0 Q 0 │
    └────────────────┘
    conflicts: 2
    step: 4
    sideways move: 0
    FAILED!
# Random Restarts Hill Climbing Results
----------
| **Runs**                  | 100      |
| ------------------------- | -------- |
| **N Queens**              | 8        |
| **Sideways Moves**        | 1 (None) |
| **Average Restarts**      | 5.28     |
| **Average Success Rate**  | 1        |
| **Average Success Steps** | 4        |
| **Average Failure Rate**  | 0        |
| **Average Failure Steps** | 0        |

| **Runs**                  | 100   |
| ------------------------- | ----- |
| **N Queens**              | 8     |
| **Sideways Moves**        | 100   |
| **Average Restarts**      | .06   |
| **Average Success Rate**  | 1     |
| **Average Success Steps** | 16.94 |
| **Average Failure Rate**  | 0     |
| **Average Failure Steps** | 0     |



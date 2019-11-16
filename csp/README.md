# Map Coloring Report

# What is the color mapping problem?
----------

The map coloring problem entails coloring map given it is divided into a select amount of distinct regions or states. Given this base we want to fill in the map so that every region or state is assigned a color, but no adjacent region or state has the same color. It turns out that the map coloring problem is actually a subset of a much more generic problem called the four color theorem. This theorem states that given a continuous plane that is divided into discrete regions there is no more than 4 colors ever needed so that no adjacent regions have the same color. It turns out this theorem’s proof was originally computer assisted thus impossible for humans to check by hand and not accepted. As of today the four color theorem still holds and is widely accepted (I believe it was even officially proved as well).

For this project we will be attempting to solve the map coloring problem for the US and AU maps.

# Algorithms
----------
## DFS

Depth-first search works by exploring the deepest nodes first. This inherently goes well with backtracking which allows DFS to inherently correct its choices if one path of the tree turns out to be a dead end (the problem is not solved). The map coloring problem, and CSP in general, use DFS in its recursive form to allow for inherent backtracking. This means that if we assign a given state a color and continue down the tree only to find that this initial assignment does not allow us to solve the problem we can backtrack (step backwards recurisively) and change the initial states color (or any states’ color that was set along the way).

## Forward Checking

DFS with backtracking is a great start but for large problems, i.e. US map coloring, it can be extremely slow. In order to add foresight to our algorithm we use forward checking. When a state is assigned a color forward checking allows us to remove said color in the neighboring states’ domains. This ensures that no state will choose a color of its neighbors. However, if we go to remove a color in a neighbor’s domain and the color to be removed is the only color left in said neighbor’s domain then we can see that our current path will fail, thus we resort to backtracking to find another path. This acts as a form of early checking, backtrack before we go further down the tree, which DFS doesn’t not typically do oh its own.

## Propagation Through Singletons

To add additional foresight to our algorithm we can add propagation through singletons.  The idea behind this algorithm is to identify states that currently have a single color in their domain and attempt to reserve said color for said single domain state. (This algorithm requires some sort of domain removal like forward checking since it is checking for states with unary domains). This entails identifying these single color states and then removing the color from said state’s neighbors. Much like forward checking, if we go to remove the single color from a neighboring state’s domain but said neighboring state only has the same single color then our problem is set to fail, we thus then backtrack. This too can act as a form of early checking, backtrack before we go further down the tree. 

# Heuristics
----------
## Random

The random heuristic is the default heuristic used for state selection. This simply means when we go to assign a state a color we choose randomly from among the pool of unassigned states.

## MRV

For a more intuitive heuristic we can select a state from the pool of unassigned states by selecting the state with the smallest domain. Since the selected state’s domain is the smallest this indicates to us that this is the most restricted state. Thus, the state with the smallest domain should be assigned a color as soon as possible. This is a great way of selecting unassigned states.

## Degree Constraint

Degree constraint is much like MRV except it chooses an unassigned state with the most constraints, i.e. most neighbors. This indicates to us that the state with the most neighbors will be the hardest state to assign a color to. Thus, we should assign it a color as soon as possible. This is typically a good way to select your initial state.

## Least Constraining Value

Instead of selecting states (variables) what about selecting colors (values)? This is where the least constraining value comes in. Least constraining value takes the current state’s domain and then counts the amount of times each color in the current state’s domain appears in the current state’s neighboring domains. By doing so, the current state can select the color with the highest count indicating that this color is the must abundantly available among its neighbors. Thus, the current state will not select a scarce color that might lead to the problem failing (i.e. needing backtracks) later on. 


# Code Structure
----------
## Running  Code

To run the program via command line simply path to the `csp/` directory and run `python .` or `python __main__.py` .

## Installing Requirements

The requirements file `requirements.txt` contains all the required packages to run my code. The following command for pip should suffice (a Conda install should work as well).

## Configuration

To select the region, number of colors, and to activate forward checking, propagation through singletons, or heuristics see the `config,yml` file.

| Parameters         | Definition                                                                                                                                                                                                                                                                                                    |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `domain_size`      | Input type: Integer<br><br>Any integer valued input will suffice. The domain size determines how many colors are available for the map coloring problem. However, assigning a domain under 4 has the potential for an unsolvable problem.                                                                     |
| `forward_checking` | Input type: Boolean<br><br>Enables forward checking if true.                                                                                                                                                                                                                                                  |
| `heuristic`        | Input type: Boolean<br><br>Enables all heuristics. This means, MRV, degree constraint and least value constraint are all activated.                                                                                                                                                                           |
| `propagation`      | Input type: Boolean<br><br>Enables propagation through singletons if true. Note, if forward checking is not enabled then this function is rather useless since it only runs if there is a single valued domain left. Thus, without forward checking all domains will always be at max potential.              |
| `region`           | Input type: String<br><br>There are two regions you can select from. The first is Australia which can be selected by inputting `au`.  The other option is the US which can be selected by inputting `us`. Any options other than these two will throw an error.                                               |
| `seed`             | Input type: Integer<br><br>Determines the seed used for randomly selecting states. If no forward checking, propagation or heuristics are used then DFS defaults to randomly selecting states. A randomly selected initial state will be used for forward checking and propagation if heuristics are disabled. |

## main.py

The `__main__.py` file is in charge of loading the config file. The only function of note here is the `region_selector` which will load the user specified region that was given in the config file. The other function, `load_config`, is for loading all yml files.

## csp.py

The `csp.py` file contains all the code for the map coloring problem, i.e. `MapColoring` the class which is in charge of running DFS, among other methods.  `MapColoring` contains code related to DFS, forward checking, propagation through singletons, consistency checks, and printing/checking of final assignments. Any code related to heuristics are located in functions outside the `MapColoring` class, but within the same file. Along with these heuristic functions are some utility functions for printing and timing code.

**Note, all colors are represented by integers. Since we do not actually have to visualize the assignments it is much simpler to work which digits instead of strings!**

**Functions**

| **Function**               | **Description**                                                                                                             |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `bordered`                 | Function used to add border around text (I do not take credit for this function as it is simply a utility).                 |
| `degree_constraint`        | Selects variable with the highest number of constraints from unassigned variables (typically used for initialization only). |
| `least_constraining_value` | Returns domain sorted by most usable value based on neighboring domains.                                                    |
| `MRV`                      | Selects variable with the smallest domain from unassigned variables.                                                        |
| `random_variable`          | Selects random variables from unassigned variables.                                                                         |
| `timeme`                   | Decorator for tracking the runtime of a function.                                                                           |


**MapColoring Class**

| **Method**          | **Description**                                                                                                                                                                     |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `__call__`          | Runs the DFS search on the map coloring problem and then prints and checks assignments.                                                                                             |
| `check_assignments` | Checks final color assignments are actually consistent (just in case something failed in the algorithm).                                                                            |
| `consistent`        | Checks for consistency of a state’s color assignment with all other neighbors that have an assignment.                                                                              |
| `dfs`               | Runs DFS along with other potential heuristics and methods (forward checking and propagation) on the map coloring problem. Uses recursive DFS to inherently allow for backtracking. |
| `forward_checking`  | Eliminates colors from neighbors when a color is selected for a given state.                                                                                                        |
| `print_info`        | Prints final color assignments and checks if assignments are actually consistent.                                                                                                   |
| `propagate`         | Eliminates colors from neighbors if a state with a single color is detected.                                                                                                        |



## Other

Other files include `au-adjacency.yml` and `us-adjacency.yml` which simply contain the constraints for each state in the given region.

# Results: US Map
## Analysis

First, this is a biased selection of seeds as some seeds like (1 or 3) never completed for DFS only search, due to the random state selection. If we simply select a random initial state and the follow the given order of the states a solution can be found within around 4-5 minutes (though this goes against the instructions so is not used). For the sake of testing I selected seeds that completed within a reasonable amount of time.

The given results are actually quite intuitive. As we added more foresight to the problem and better heuristics the amount of time and backtracks decreases. The best results in terms of time and backtracks was **DFS + forward checking with heuristics.** However, **DFS + forward checking + propagation through singletons with heuristics** achieved the same time and backtracks with a negligible difference. On a even more complex problem I would suspect **DFS + forward checking + propagation through singletons with heuristics** would beat out **DFS + forward checking with heuristics.**  

An interesting note is that **DFS with no heuristics** solves some seeds within a reasonable amount of time and others, like seeds 1 and 3, in no so reasonable amounts of time. But, as soon as we add heuristics or forward checking all seeds are solved within in seconds and even milliseconds. This truly goes to show how powerful these algorithms are.

## No heuristics

**DFS** 

| **Trials**  | **Times (Seconds)** | **Backtracks** |
| ----------- | ------------------- | -------------- |
| 1 (seed 2)  | 15.61               | 10737808       |
| 2 (seed 5)  | 2.21                | 951498         |
| 4 (seed 10) | 21.87               | 14144030       |
| 3 (seed 12) | 71.115              | 46196135       |

**DFS + forward checking**

| **Trials**  | **Times** | **Backtracks** |
| ----------- | --------- | -------------- |
| 1 (seed 2)  | 4.37      | 236880         |
| 2 (seed 5)  | 0.339     | 16921          |
| 4 (seed 10) | 0.0026    | 2              |
| 3 (seed 12) | 11.67     | 454906         |


**DFS + forward checking + propagation through singletons**

| **Trials**  | **Times**   | **Backtracks** |
| ----------- | ----------- | -------------- |
| 1 (seed 2)  | 0.720077290 | 8047           |
| 2 (seed 5)  | 0.005356815 | 0              |
| 4 (seed 10) | 0.005901614 | 0              |
| 3 (seed 12) | 0.005922089 | 0              |


**Averages**

| **Type**                                                | **Time** | **Backtracks** |
| ------------------------------------------------------- | -------- | -------------- |
| DFS                                                     | 27.701   | 18007367.75    |
| DFS + forward checking                                  | 4.0954   | 117117.25      |
| DFS + forward checking + propagation through singletons | .184293  | 2011.75        |

## Heuristics

Since degree constraint is used all states will start from the same initial state, i.e. all trials no matter the seed will be the same (run time will of course vary slightly between trials).

**DFS**

| **Trials**  | **Times**   | **Backtracks** |
| ----------- | ----------- | -------------- |
| 1 (seed 2)  | 0.155127647 | 73588          |
| 2 (seed 5)  | 0.156794111 | 73588          |
| 4 (seed 10) | 0.155127647 | 73588          |
| 3 (seed 12) | 0.156794111 | 73588          |

**DFS + forward checking**

| **Trials**  | **Times**   | **Backtracks** |
| ----------- | ----------- | -------------- |
| 1 (seed 2)  | 0.003596583 | 0              |
| 2 (seed 5)  | 0.003847145 | 0              |
| 4 (seed 10) | 0.003542503 | 0              |
| 3 (seed 12) | 0.003718548 | 0              |


**DFS + forward checking + propagation through singletons**

| **Trials**  | **Times**   | **Backtracks** |
| ----------- | ----------- | -------------- |
| 1 (seed 2)  | 0.004476245 | 0              |
| 2 (seed 5)  | 0.004532791 | 0              |
| 4 (seed 10) | 0.004458360 | 0              |
| 3 (seed 12) | 0.004452705 | 0              |


**Average**

| **Type**                                                | **Time**   | **Backtracks** |
| ------------------------------------------------------- | ---------- | -------------- |
| DFS                                                     | .15596066  | 73588          |
| DFS + forward checking                                  | .003676135 | 0              |
| DFS + forward checking + propagation through singletons | .00449825  | 0              |

# Results: AU Map
----------
## Analysis

Unlike the US map all results here are actually not as intuitive as you would expect. If we look at optimal run time **DFS with heuristics** wins. But, if we look at number of backtracks needed then 
**DFS + forward checking + propagation through singletons with heuristics** and **DFS + forward checking with heuristics** win. The reason **DFS with heuristics** wins in run time even though it has more backtracks is because it is a simpler algorithm that does not run nearly as many loops. Also, since the overall problem is simpler as well (i.e. less states) then it make errors and backtracking faster than using foresight. Thus, on simpler problems, like the AU map coloring, **DFS with heuristics** might be the best go to algorithm to get a fewer number of backtracks and optimal time.

## No heuristics

**DFS** 

| **Trials** | **Times (Seconds)** | **Backtracks** |
| ---------- | ------------------- | -------------- |
| 1 (seed 1) | 0.000215647         | 76             |
| 2 (seed 2) | 0.000161601         | 4              |
| 4 (seed 3) | 0.000205848         | 67             |
| 3 (seed 4) | 0.000149482         | 5              |

**DFS + forward checking**

| **Trials** | **Times**   | **Backtracks** |
| ---------- | ----------- | -------------- |
| 1 (seed 1) | 0.000927220 | 22             |
| 2 (seed 2) | 0.000324053 | 0              |
| 4 (seed 3) | 0.000565783 | 9              |
| 3 (seed 4) | 0.000356252 | 0              |


**DFS + forward checking + propagation through singletons**

| **Trials** | **Times**   | **Backtracks** |
| ---------- | ----------- | -------------- |
| 1 (seed 1) | 0.001171258 | 10             |
| 2 (seed 2) | 0.000484559 | 0              |
| 4 (seed 3) | 0.000802184 | 3              |
| 3 (seed 4) | 0.000545241 | 0              |


**Averages**

| **Type**                                                | **Time**   | **Backtracks** |
| ------------------------------------------------------- | ---------- | -------------- |
| DFS                                                     | .00018311  | 38             |
| DFS + forward checking                                  | .000543275 | 7.75           |
| DFS + forward checking + propagation through singletons | .00075075  | 3.25           |

## Heuristics

Since degree constraint is used all states will start from the same initial state, i.e. all trials no matter the seed will be the same (run time will of course vary slightly between trials).

**DFS**

| **Trials** | **Times**   | **Backtracks** |
| ---------- | ----------- | -------------- |
| 1 (seed 1) | 0.000151196 | 7              |
| 2 (seed 2) | 0.000151695 | 7              |
| 4 (seed 3) | 0.000155691 | 7              |
| 3 (seed 4) | 0.000184551 | 7              |

**DFS + forward checking**

| **Trials** | **Times**   | **Backtracks** |
| ---------- | ----------- | -------------- |
| 1 (seed 1) | 0.000441860 | 0              |
| 2 (seed 2) | 0.000459095 | 0              |
| 4 (seed 3) | 0.000420395 | 0              |
| 3 (seed 4) | 0.000415216 | 0              |


**DFS + forward checking + propagation through singletons**

| **Trials** | **Times**   | **Backtracks** |
| ---------- | ----------- | -------------- |
| 1 (seed 1) | 0.000706916 | 0              |
| 2 (seed 2) | 0.000591561 | 0              |
| 4 (seed 3) | 0.000596488 | 0              |
| 3 (seed 4) | 0.000579309 | 0              |


**Average**

| **Type**                                                | **Time**   | **Backtracks** |
| ------------------------------------------------------- | ---------- | -------------- |
| DFS                                                     | .00018295  | 7              |
| DFS + forward checking                                  | .000329    | 0              |
| DFS + forward checking + propagation through singletons | .000618525 | 0              |

# Example Output:

Output of the program will look something like below, depending on the region selected. If you want to manually check assignments each state with its color is printed. Underneath each state is a array of colors, represented by numbers.  Simply look at the state and its neighboring colors to manually check. 


> Initial State: South Australia
> South Australia color: 0
>          Neighboring colors: [1, 2, 1, 2, 1]
> Western Australia color: 1
>          Neighboring colors: [2, 0]
> Northern Territory color: 2
>          Neighboring colors: [1, 0, 1]
> Queensland color: 1
>          Neighboring colors: [2, 0, 2]
> New South Wales color: 2
>          Neighboring colors: [0, 1, 1]
> Victoria color: 1
>          Neighboring colors: [0, 2]
> Tasmania color: 0
>          Neighboring colors: []
> Backtacks: 0
> Assignments are consistent!
> 


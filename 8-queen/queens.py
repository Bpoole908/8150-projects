from pdb import set_trace

import numpy as np

def boarder(text):
    """ Simply adds a border to any passed string.
        
        Args:
            test (str): Desired string to add boarder to.
        
        Returns:
            A string with a boarder surronding it
    """
    l = text.splitlines()
    w = max(len(s) for s in l)
    wrapper = ['┌' + '─' * w + '┐']
    for s in l:
        wrapper.append('│' + (s + ' ' * w)[:w] + '│')
    wrapper.append('└' + '─' * w + '┘')

    return '\n'.join(wrapper)

class Queens(object):
    """ Queens is in charge of the N-queens problem which means maintaining the 
        board, generating neighbors and calculating the number of conflicts.

        Attributes:
            n (int): Number of queens which determines size of the board.

            board (ndarray): Internal state of the current board, which is 
                typically changed by forces outside the class.
    """
    def __init__(self, n):
        self.n = n
        self.board = None # internal state of the current board
    
    def populate_board(self, seed=1):
        """ Populates a [n, n] board given a random seed.
        
            Args:
                seed (int): Seed for randomization.
        """
        self.board = np.zeros([self.n, self.n], dtype=np.uint8)
        
        np.random.seed(seed)
        for row in range(self.n):
            col = np.random.randint(self.n)
            self.board[row, col] = 1

    def print_board(self, empty='0', queen='Q'):
        """ Prints the board in a clean but slower fashion.

            Args:
                empty (str): Symbol to represent empty space.

                queen (str): Symbol to represent the queens.
        """
        board = ''
        for row in self.board:
            for i, idx in enumerate(row):
                if idx == 0:
                   board += '{} '.format(empty)
                else:
                    board += '{} '.format(queen)
            board += '\n'
        print(boarder(board))
    
    def coords_to_board(self, coords):
        """ Translates all passed queen coordinates to board form. 

            Args:
                coords (ndarray): Numpy array of N queen coordinates.
            
            Returns:
                A [n, n] board with queens at passed coordinates.
        """
        board = np.zeros([self.n, self.n], dtype=np.uint8)
        for row, col in coords:
            board[row, col] = 1
        
        return board

    def get_coords(self):
        """ Gets all coordinates (row, col) for queens on the board.

            Returns:
                (n, 2) ndarray of queen coordinates where rows are the 
                y coordinates columns are the x coordinates. 
        """
        locs = np.where(self.board == 1)
        return np.hstack([locs[0].reshape(-1,1), locs[1].reshape(-1,1)])

    def queen_conflicts(self, queen, coords):
        """ Check for a single queen's conflicts given all other queen’s coordinates.

            Args:
                queen (ndarray): Coordinates for a single queen (row, col).

                coords (ndarray): Coordiantes for all other queens (row, col).
            
            Returns:
                Total conflicts queen has ONLY

        """
        queen_conflicts = 0

        # Diagonal checks
        diag_check = np.abs(queen -  coords)
        diag_check = diag_check[:, 0] - diag_check[:, 1]
        queen_conflicts += len(np.where(diag_check==0)[0])

        # Row check
        row_conflicts = len(coords[coords[:, 0] == queen[0]])
        queen_conflicts += row_conflicts

        # Column check
        col_conflicts = len(coords[coords[:, 1] == queen[1]])
        queen_conflicts += col_conflicts

        return queen_conflicts

    def heuristic(self, queen_coords=None):
        """ Calculates total number of conflicts given passed coordinates or
            from the current board.

            Args:
                queen_coords (ndarray): All queen coordinates (row, col)
            
            Returns:
                Total number of conflicts given queen_coords
        """
        total_conflicts = 0

        if queen_coords is None:
            queen_coords = self.get_coords()

        for i, queen in enumerate(queen_coords):
            coords = queen_coords[i+1:]
            
            queen_conflicts = self.queen_conflicts(queen=queen, coords=coords)
            
            total_conflicts += queen_conflicts
            # print("Queen: {} Conflicts: {}/{}".format(
            #     queen, queen_conflicts, total_conflicts))

        return total_conflicts
    
    def neighbors(self):
        """ Generates all neighbors from the current board state."""
        neighbors = []
        conflicts = []
        queen_coords = self.get_coords()

        # Loop through each queen in the board selecting each queen as the target
        # queen and determining all the neighboring ROW moves.
        for i, queen in enumerate(queen_coords):
            # Remove target queen from set of all queen coordinates
            coords = np.delete(queen_coords, i, axis=0).reshape(-1,2)

            # Determine all possible new row moves for target queen
            cols = np.arange(self.n)
            cols = np.delete(cols, queen[1]).reshape(-1, 1)

            # Create new coordinates for all possible moves for target queen
            neighbor_coords = np.hstack([np.full(cols.shape, queen[0]), cols])

            # Calculate all conflicts without target queen yet
            base_conflicts = self.heuristic(queen_coords=coords)

            # Calculate all conflicts moving target queen creates
            for new_queen in neighbor_coords:
                new_conflicts = self.queen_conflicts(queen=new_queen, coords=coords)
                total_conflicts = new_conflicts + base_conflicts
                neighbors.append(np.vstack([new_queen, coords]))
                conflicts.append(total_conflicts)

        return neighbors, conflicts

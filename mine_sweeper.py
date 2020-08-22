import random

from functools import reduce
from typing import List, Tuple

class MineSweeper:
    """Minesweeper class that starts a minesweeping game.

    The condition to win the game is to sweep all cells, except those
    with mines.

    When the user sweeps on a cell that does not have mines, this calss will tell
    the user how many mines that are adjacent to this cell, by showing a number.
    If there is no adjacent mines, the mine_sweeper class will automatically "sweep"
    those adjacent cells that are known to have no mines.

    """
    def __init__(self, board_size: int = 50, number_of_mines: int = 10):
        """Initialization of minesweeper.

        Args:
            board_size (int): Width/Height of board.
            number_of_mines (int): Number of mines.

        """
        self.board_size: int = board_size  # Size of the square gameboard.
        self.number_of_mines: int = number_of_mines  # Number of mines.
        self.seen_cells: int = 0  # Number of cells users have sweeped.
        self.has_stepped_on_mine: bool = False  # Whether the player has stepped on mine.

        # Gameboard boolean that says whether a mine exists in a cell.
        self.game_board: List[List[bool]] = [
            [False for i in range(self.board_size)] for j in range(self.board_size)]

        # Randomly sample indices to create m mines.
        all_indices: List(Tuple(int, int)) = reduce(
            lambda x, y: x + y,
            [[(i, j) for j in range(self.board_size)] for i in range(self.board_size)])
        mines: List(Tuple(int, int)) = random.sample(all_indices, self.number_of_mines)
        for (x, y) in mines:
            self.game_board[x][y] = True

        # Gameboard that player sees. "" means the user hasn't seen this cell; Positive number
        # means the number of mines around this cell; "M" means the user has sweeped a cell with
        # mine.
        self.visualization_board: List[List[str]] = [
            ["" for i in range(self.board_size)] for j in range(self.board_size)]

        self.game_over = False


    def _sweep(self, x: int, y: int):
        """Clicking on a particular cell, (x, y).

        It will show the number of cells adjacent to (x, y) that are mines. If (x, y) has a mine,
        then show "M", which means user has sweeped a mine.

        If the cell has no neighboring mines, then it will automatically sweep its neighbors.

         Args:
            x (int): Row to click.
            y (int): Column to click.

        """
        if x < 0 or x >= self.board_size or y < 0 or y >= self.board_size:
            print("Invalid entries.")
            return

        if not self.visualization_board[x][y] == "":
            print("Cell already visited.")
            return

        # delta_x/y of adjacent cells.
        delta_x = [-1, -1, -1, 0, 0, 1, 1, 1]
        delta_y = [-1, 0, 1, -1, 1, -1, 0, 1]

        cells_to_sweep = [(x, y)]
        while cells_to_sweep:
            x, y = cells_to_sweep.pop()
            if self.game_board[x][y]:  # Check if it is a mine.
                self.has_stepped_on_mine = True
                # If stepped on a mine, show ALL mines' positions
                for t in range(self.board_size):
                    for q in range(self.board_size):
                        if self.game_board[t][q]:
                            self.visualization_board[t][q] = "M"
                return
            else:
                # If this cell has already been sweeped, then continue.
                if not self.visualization_board[x][y] == "":
                    continue
                self.seen_cells += 1
                # Iterate through its neighbors and count number of mines.
                count = 0
                valid_neighbors: List[Tuple[int, int]] = []
                for i in range(7):
                    new_x = x + delta_x[i]
                    new_y = y + delta_y[i]
                    if (new_x < 0 or new_x >= self.board_size
                        or new_y< 0 or new_y >= self.board_size):
                        continue
                    valid_neighbors.append((new_x, new_y))
                    count += self.game_board[new_x][new_y]
                if not count == 0:
                    self.visualization_board[x][y] = str(count)
                else:
                    # If there is no mine in the neighbor, automatically click all neighbors.
                    self.visualization_board[x][y] = "0"
                    for neighbor in valid_neighbors:
                        if self.visualization_board[neighbor[0]][neighbor[1]] == "":
                            cells_to_sweep.append((neighbor[0], neighbor[1]))


    def _visualize(self):
        """Visualize the board.

        The visualization includes the name, the horizontal header,
        the vertical header, and each cell.

        An example would be the following:

                        MineSweeper

                   0    1    2    3    4
               _________________________
               |    |    |    |    |    |
            0  | 0  | 0  | 0  | 1  |    |
               |____|____|____|____|____|
               |    |    |    |    |    |
            1  | 1  | 1  | 0  | 1  | 1  |
               |____|____|____|____|____|
               |    |    |    |    |    |
            2  |    | 1  | 0  | 0  | 0  |
               |____|____|____|____|____|
               |    |    |    |    |    |
            3  | 1  | 1  | 0  | 0  | 0  |
               |____|____|____|____|____|
               |    |    |    |    |    |
            4  | 0  | 0  | 0  | 0  | 0  |
               |____|____|____|____|____|

        """
        cell_width = 5
        left_margin = 3

        print()
        print(" " * int(cell_width * self.board_size / 2) + "MineSweeper")
        print()

        # Drawing the horizontal header.
        horizontal_header = " " * left_margin
        for i in range(self.board_size):
            horizontal_header = horizontal_header + " " * (cell_width - len(str(i))) + str(i)
        print(horizontal_header)

        for i in range(self.board_size):
            st = " " * left_margin
            if i == 0:
                for _ in range(self.board_size):
                    st = st + "_" * cell_width
                print(st)

            # Drawing the first line of each cell.
            st = " " * left_margin
            for _ in range(self.board_size):
                 st = st + "|" + " " * (cell_width - 1)
            print(st + "|")

            # Drawing the second line of each cell, it also contains the vertical header.
            st = str(i) + " " * (left_margin - len(str(i)))
            for j in range(self.board_size):
                # If visualization_board[i][j] is a number or "M", we can draw 1 less space.
                # But if it is "", we still need to draw the space.
                st = (st + "|" + " " + self.visualization_board[i][j] +
                      " " * (cell_width - 2 - len(self.visualization_board[i][j])))
            print(st + "|")

            # Drawing the third line of each cell.
            st = " " * left_margin
            for _ in range(self.board_size):
                st = st + "|" + "_" * (cell_width - 1)
            print(st + '|')
        print()


    def play(self, x: int, y: int):
        """Clicking on a particular cell, (x, y), wrapper of _click.

        The function calls _click and check whether the game is over.

         Args:
            x (int): Row to click.
            y (int): Column to click.

        """
        if self.game_over:
            print("Game is already over.")

        self._sweep(x, y)
        self._visualize()

        if self.has_stepped_on_mine:
            self.game_over = True
            print("You lost the game.")

        if self.seen_cells == self.board_size * self.board_size - self.number_of_mines:
            self.game_over = True
            print("You won!")


if __name__ == "__main__":
    m = MineSweeper(10, 15)
    while not m.game_over:
        print("Enter x and y, separated by space, eg \"1 3\":")
        user_inputs = input()
        indices = user_inputs.split()
        if not len(indices) == 2:
            print("Please enter two indices, separated by space.")
            continue
        if (not indices[0].isdigit()) or (not indices[1].isdigit()):
            print("Please enter valid indices.")
            continue
        m.play(int(indices[0]), int(indices[1]))


from typing import List, Tuple, Optional
import sys
from mocks import ReversiStub, BoardGridType

# Characters for drawing the board
WALL_CHARS = {
    "H_WALL": "─", "V_WALL": "│", "HV_WALL": "┼",
    "NW_CORNER": "┌", "NE_CORNER": "┐", "SW_CORNER": "└", "SE_CORNER": "┘",
    "VE_WALL": "├", "VW_WALL": "┤", "HS_WALL": "┬", "HN_WALL": "┴",
    "N_WALL": "╵", "E_WALL": "╶", "S_WALL": "╷", "W_WALL": "╴"
}

#boolean representations of WALL_CHARS
CLOCK_CHARS = {
    (False, False, False, False): " ",
    (False, False, False, True): WALL_CHARS["W_WALL"],
    (False, False, True, False): WALL_CHARS["S_WALL"],
    (False, False, True, True): WALL_CHARS["NE_CORNER"],
    (False, True, False, False): WALL_CHARS["E_WALL"],
    (False, True, False, True): WALL_CHARS["H_WALL"],
    (False, True, True, False): WALL_CHARS["NW_CORNER"],
    (False, True, True, True): WALL_CHARS["HS_WALL"],
    (True, False, False, False): WALL_CHARS["N_WALL"],
    (True, False, False, True): WALL_CHARS["SE_CORNER"],
    (True, False, True, False): WALL_CHARS["V_WALL"],
    (True, False, True, True): WALL_CHARS["VW_WALL"],
    (True, True, False, False): WALL_CHARS["SW_CORNER"],
    (True, True, False, True): WALL_CHARS["HN_WALL"],
    (True, True, True, False): WALL_CHARS["VE_WALL"],
    (True, True, True, True): WALL_CHARS["HV_WALL"]
}

side: int = int(sys.argv[1])
game: ReversiStub = ReversiStub(side, 2, False)
grid: BoardGridType = game.grid

#turn the grid into a string
def to_string(board: BoardGridType) -> str:
    """
    Returns a string representation of the game board
    Args:
        board: the game board
    Returns: String representation
    """
    #first construct an empty grid to fill in
    n: int = 2 * len(board) + 1
    str_grid: List[List[str]] = [[" "] * n for _ in range(n)]

    #draw the boundaries of the squares
    for k, grid_row in enumerate(str_grid):
        for l, entry in enumerate(grid_row):
            #draw the boundaries of the squares in diagonal directions
            if k % 2 == 0 and l % 2 == 0:
                m = n - 1
                str_grid[k][l] = CLOCK_CHARS[(k > 0, l < m, k < m, l > 0)]
            #draw the boundaries of the squares in cardinal directions
            elif k % 2 == 0:
                str_grid[k][l] = CLOCK_CHARS[(False, True, False, True)]
            elif l % 2 == 0:
                str_grid[k][l] = CLOCK_CHARS[(True, False, True, False)]

    #fill in the pieces
    for i, board_row in enumerate(board):
        for j, square in enumerate(board_row):
            if not square is None:
                str_grid[2 * i + 1][2 * j + 1] = str(square)

    #turn str_grid into a string
    rv: List[str] = [""] * n
    for k, grid_row in enumerate(str_grid):
        rv[k] = "".join(grid_row)
    return "\n".join(rv)

print(to_string(grid))

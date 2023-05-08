from typing import List, Tuple, Optional
import sys
from reversi import Reversi, Board, BoardGridType

BOARD_SIZE: int = int(sys.argv[1])
game: Reversi = Reversi(BOARD_SIZE, 2, True)

while not game.done:
    print(game)
    proceed: bool = False
    while not proceed:
        print(f"It is Player {game.turn}'s turn. Please choose a move:")
        print()
        for i, (j, k) in enumerate(game.available_moves):
            print(f"{i + 1}) {j}, {k}")
        print()
        inp: str = input(">")
        try:
            idx: int = int(inp) - 1
            if idx in range(len(game.available_moves)):
                move = game.available_moves[idx]
                proceed = True
            else:
                continue
        except:
            continue
    game.apply_move(move)
    if game.done:
        winners: str = ", ".join([str(val) for val in game.outcome])
        print("The game is done. The winners are players " + winners + ".")

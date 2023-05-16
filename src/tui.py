from typing import List, Tuple, Optional
import click
import sys
from reversi import Reversi, Board, BoardGridType


@click.command("tui")
@click.option("-n", "--num-players", default = 2)
@click.option("-s", "--board-size", default = 8)
@click.option("--othello", is_flag = True)
@click.option("--non-othello", is_flag = True)
def run_game(num_players: int, board_size: int, othello: bool, 
             non_othello: bool) -> None:
    try:
        game: Reversi = Reversi(board_size, num_players, not non_othello)
    except Exception as e:
        print(e)
        sys.exit()

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
    print(game)
    winners: str = ", ".join([str(val) for val in game.outcome])
    print("The game is done.")
    if len(winners) == 1:
        print("Player " + winners + " wins.")
    else:
        print("Players " + winners + " win.")

if __name__ == "__main__":
    run_game()

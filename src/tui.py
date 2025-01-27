from typing import List, Tuple, Optional
import click
import sys
from reversi import Reversi, Board, BoardGridType, COLORS
from bot import ReversiBot
from termcolor import colored, cprint

@click.command("tui")
@click.option("-n", "--num-players", default = 2)
@click.option("-s", "--board-size", default = 8)
@click.option("--othello", is_flag = True)
@click.option("--non-othello", is_flag = True)
@click.option("--bot",
              type = click.Choice(["random", "smart", "very-smart"]),
              default = None)
def run_game(num_players: int, board_size: int, othello: bool, 
             non_othello: bool, bot: Optional[str]) -> None:
    try:
        game: Reversi = Reversi(board_size, num_players, not non_othello)
    except Exception as e:
        print(e)
        sys.exit()
    game_bot: ReversiBot = ReversiBot(game)

    while not game.done:
        if (bot is None) or game.turn == 1:
            print(game)
            proceed: bool = False
            while not proceed:
                col_turn: str = colored(str(game.turn), COLORS[game.turn])
                print(f"It is Player {col_turn}'s turn. Please choose a move:")
                print()
                for i, (j, k) in enumerate(game.available_moves):
                    print(f"{i + 1}) {j}, {k}")
                print("For a hint enter 'hint'.")
                print()
                inp: str = input(">")
                if inp == "hint":
                    i, j = game_bot.hint("very-smart")
                    print(f"Try {i}, {j}.")
                    print()
                    continue
                try:
                    idx: int = int(inp) - 1
                    if idx in range(len(game.available_moves)):
                        move: Tuple[int, int] = game.available_moves[idx]
                        proceed = True
                    else:
                        continue
                except:
                    continue
            game.apply_move(move)
        if (not bot is None) and game.turn != 1:
            print(game)
            i, j = game_bot.hint(bot)
            col_turn = colored(str(game.turn), COLORS[game.turn])
            print(f"Player {col_turn} ({bot} bot) makes the move {i}, {j}.")
            game_bot.move(bot)
            
    print(game)
    winners: List[str] = [colored(str(x), COLORS[x]) for x in game.outcome]
    winners_str: str = ", ".join(winners)
    print("The game is done.")
    if len(winners) == 1:
        print("Player " + winners_str + " wins.")
    else:
        print("Players " + winners_str + " win.")

if __name__ == "__main__":
    run_game()

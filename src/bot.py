"""
Bots for Reversi
(and command for running simulations with bots)
"""

import random
import sys
from typing import Union

from mocks import ReversiStub

#
# BOTS
#

class ReversiBot:
    """
    Gets the moves for a single player
    """

    def __init__(self, player, stub: ReversiStub) -> None:
        self.player = player
        self.stub = stub
    
    def get_move(self):
        moves = self.stub.available_moves
        if len(moves) > 0:
            move = random.choices(moves)
            return move[0]
    
def play_game(player1: ReversiBot, player2: ReversiBot, game: ReversiStub):
    while len(game.outcome) < 2:
        if game.turn == 1:
            move = player1.get_move()
            if move is not None:
                game.apply_move(move)
            else:
                game._turn = 2
        elif game.turn == 2:
            move = player2.get_move()
            if move is not None:
                game.apply_move(move)
            else:
                game._turn = 1
    return game.outcome 
    
def play_num_games(numgames):
    player1_wins = 0
    player2_wins = 0
    draws = 0
    for i in range(numgames):
        board = ReversiStub (8,2, False)
        player1 = ReversiBot(1, board)
        player2 = ReversiBot(2, board)
        result = play_game(player1, player2, board)
        if result[0] == 1:
            player1_wins += 1
        if result[0] == 2:
            player2_wins += 1
        if result[1] == 1:
            draws += 1
    player1_perc = (player1_wins / numgames) * 100
    player2_perc = (player2_wins / numgames) * 100
    draw_perc = (draws / numgames) * 100

    print (f"Player 1 wins: {player1_perc}")
    print (f"Player 2 wins: {player2_perc}")
    print (f"Ties: {draw_perc}")


def main():
    numgame = int(sys.argv[1])
    play_num_games(numgame)

main()






    
    

    

    



    
 


    
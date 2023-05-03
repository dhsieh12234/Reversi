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

    def __init__(self, player) -> None:
        self.player = player
        self.game = ReversiStub(8, 2, False)
        self.numgame = int(sys.argv[1])
    
    def apply_move(self):
        moves = self.game.available_moves()
        if len(moves) > 0:
            move = random.choices(moves)
            self.game.apply_move(move)
            print (self.game)
        else:
            None
    
    def play_game(self):
        while len(self.game.outcome()) < 2:
            self.apply_move()
        return self.game.outcome() 
    
    def play_num_games(self):
        player1_wins = 0
        player2_wins = 0
        draws = 0
        for i in range(self.numgame):
            result = self.play_game()
            if result[0] == 1:
                player1_wins += 1
            if result[0] == 2:
                player2_wins += 1
            if result[1] == 1:
                draws += 1
        player1_perc = player1_wins / self.numgame
        player2_perc = player2_wins / self.numgame
        draw_perc = draws / self.numgame

        print (f"Player 1 wins: {player1_perc}")
        print (f"Player 2 wins: {player2_perc}")
        print (f"Ties: {draw_perc}")






    
    

    

    



    
 


    
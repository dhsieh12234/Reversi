"""
Bots for Reversi
(and command for running simulations with bots)
"""

import random
import sys
from typing import Union, Tuple, Optional 

from mocks import ReversiStub, ReversiBotMock

#
# BOTS
#

class ReversiBot:
    """
    Gets a random for the bot to act upon
    """

    def __init__(self, player: int, stub: ReversiBotMock) -> None:
        """
        Constructor

        Args: 
            player: the player whos moves you are finding
            stub: the grid of the current game
        """
        self.player = player
        self.stub = stub
        if self.player == 1:
            self.type = "optimizer"
        else:
            self.type = "random"
    
    def get_move(self) -> Optional[Tuple[int,int]]:
        """
        From a set of avalible moves that can be taken by the player, 
        one move is chosen from the list of moves
        
        Returns:
            a desired move by the player, or None of there is not player

        """
        if self.type == "optimizer":
            move = self.stub.choose_move()
            # print (f"optimal move {move}")
            print (f"player: {self.type}")
            # print (f"new player: {self.type}")
            return move
        if self.type == "random":
            moves = self.stub.available_moves
            if len(moves) == 0:
                return None
            move = random.choices(moves)
            # print (f"player: {self.type}")
            print (f"random move {move}")
            # print (f"new player: {self.type}")
            return move[0]


    
def play_game(player1: ReversiBot, player2: ReversiBot, game: ReversiBotMock) -> list[int]:
    """
    Play one singular game of ReversiStub which ends when either 4 moves have
    been taken or a player hits (0,0)

    Args:
        player1: the first player of the game
        player2: the second player of the game
        game: the board that keeps track of the moves
    
    Returns
        the outcome of game, whether it was a draw, win by player1 or win by
        player 2
    """
    while not (len(game.outcome) == 1 or len(game.outcome) == 2):
        print ("\n")
        print ("NEW TURN")
        if game.turn == 1:
            print ("Hello")
            move = player1.get_move()
            print (f"player 1 move: {move}")
            if move is not None:
                game.apply_move(move)
            else:
                game.turn = 2
        elif game.turn == 2:
            print ("Hello")
            move = player2.get_move()
            print (f"player 2 move: {move}")
            if move is not None:
                game.apply_move(move)
            else:
                game.turn = 1
    return game.outcome 
    
def play_num_games(numgames: int) -> None:
    """
    Play a specific number of Reversi games specified by the user

    Args:
        numgames: the amount of times the game should be played
    """
    player1_wins = 0
    player2_wins = 0
    draws = 0
    for i in range(numgames):
        board = ReversiBotMock (8,2, False)
        player1 = ReversiBot(1, board)
        player2 = ReversiBot(2, board)
        result = play_game(player1, player2, board)
        print (result)
        if result[0] == 1:
            player1_wins += 1
        if result[0] == 2:
            player2_wins += 1
        if len(result) == 2:
            draws += 1
    player1_perc = round(((player1_wins / numgames)* 100),2)
    player2_perc = round(((player2_wins / numgames)* 100),2)
    draw_perc = round(((draws / numgames) * 100),2)

    print (f"Player 1 wins: {player1_perc}%")
    print (f"Player 2 wins: {player2_perc}%")
    print (f"Ties: {draw_perc}%")


def main():
    numgame = int(sys.argv[1])
    play_num_games(numgame)

main()

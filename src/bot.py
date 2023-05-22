"""
Bots for Reversi
(and command for running simulations with bots)
"""

import random
import sys
from typing import Union, Tuple, Optional, List
import click
import time


from mocks import ReversiStub, ReversiBotMock
from reversi import Reversi, Piece, Board, ReversiBase


#
# BOTS
#
class RandomBot:
    """
    Simple Bot that just picks a move at random
    """

    _reversi: Reversi

    def __init__(self, reversi: Reversi):
        """ Constructor

        Args:
            reversi: The game that the bot plays in
        """
        self._reversi = reversi

    def suggest_move(self) -> Tuple[int, int]:
        """ Suggests a move

        Returns: None

        """
        moves = self._reversi.available_moves
        return random.choice(moves)

class SmartBot:
    """
    Smart bot that chooses move based off amount of captured pieces
    """

    _reversi: Reversi

    def __init__(self, reversi: Reversi):
        """ Constructor

        Args:
            reversi: The game that the bot plays in
        """
        self._reversi = reversi

    def suggest_move(self) -> Tuple[int, int]:
        """ Suggests a move

        Returns: None

        """
        moves = self._reversi.available_moves
        capture_counts = [len(self._reversi.captures(move)) for move in moves]
        max_capture = max(capture_counts)
        optimal_moves = []
        for i, x in enumerate(capture_counts):
            if x == max_capture:
                optimal_moves.append(moves[i])
        return random.choice(optimal_moves)


class VerySmartBot:
    """
    Simple Bot that just picks a move at random
    """

    _reversi: Reversi

    def __init__(self, reversi: Reversi):
        """ Constructor

        Args:
            reversi: The game that the bot plays in
        """
        self._reversi = reversi


    def suggest_move(self) -> Tuple[int, int]:
        """ Suggests a move

        Returns: None

        """   
        
        def find_average(list):
            sum = 0
            for num in list:
                sum += num
            return sum / (len(list))

        moves = self._reversi.available_moves
        player = self._reversi.turn
        dif_values = []
        for move1 in moves:
            sim_game: Reversi = self._reversi.simulate_moves([move1])
            
            #check if move1 wins the game
            winners = sim_game.outcome
            if len(winners) == 1 and winners[0] == player:
                return move1
            
            #maximize value
            #we count the pieces captured by move1 and move2
            # not the total number of pieces on the board
            piece_count_difs: List[int] = []
            for move2 in sim_game.available_moves:
                captures1: int = len(self._reversi.captures(move1))
                captures2: int = len(sim_game.captures(move2, [player]))
                dif: int = captures1 - captures2
                piece_count_difs.append(dif)
            dif_values.append(find_average(piece_count_difs))
        max_value = max(dif_values)
        optimal_moves = []
        for i, x in enumerate(dif_values):
            if x == max_value:
                optimal_moves.append(moves[i])
        return random.choice(optimal_moves)

class ReversiBot:
    """
    A class which contains all 3 of the bots at once.
    """

    game: Reversi
    rand: RandomBot
    smart: SmartBot
    very_smart: VerySmartBot

    def __init__(self, reversi: Reversi) -> None:
        """
        Constructor

        Args: 
            game: the Reversi game in question

        Methods:
            hint(bot: str): returns the move supplied by the given bot.
            move(bot: str): applies the hinted move.
        """
        self.game = reversi
        self.rand = RandomBot(reversi)
        self.smart = SmartBot(reversi)
        self.very_smart = VerySmartBot(reversi)

    def hint(self, bot: str) -> Tuple[int, int]:
        if bot == "random":
            suggested_move: Tuple[int, int] = self.rand.suggest_move()
        if bot == "smart":
            suggested_move = self.smart.suggest_move()
        if bot == "very-smart":
            suggested_move = self.very_smart.suggest_move()
        return suggested_move
    
    def move(self, bot: str) -> None:
        self.game.apply_move(self.hint(bot))

    
def play_game(bot1: str, bot2: str, game: Reversi) -> list[int]:
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

    game_bot: ReversiBot = ReversiBot(game)
    while not (len(game.outcome) == 1 or len(game.outcome) == 2):
        if game.turn == 1:
            game_bot.move(bot1)
        elif game.turn == 2:
            game_bot.move(bot2)
    return game.outcome 
    

@click.command("bot")
@click.option('-n', '--num-games', type=int, default=100)
@click.option('-1', '--player1', \
    type=click.Choice(['random', 'smart', 'very-smart']), default='random')
@click.option('-2', '--player2', \
    type=click.Choice(['random', 'smart', 'very-smart']), default='random')

def main(num_games: int, player1: str, player2: str):
    play_num_games(num_games, player1, player2)

def play_num_games(numgames: int, player1: str, player2: str) -> None:
    """
    Play a specific number of Reversi games specified by the user

    Args:
        numgames: the amount of times the game should be played
    """
    player1_wins = 0
    player2_wins = 0
    draws = 0
    for i in range(numgames):
        result = play_game(player1, player2, Reversi(8, 2, True))
        if len (result) == 1:  
            if result[0] == 1:
                player1_wins += 1
            elif result[0] == 2:
                player2_wins += 1
        if len(result) == 2:
            draws += 1
    player1_perc = round(((player1_wins / numgames)* 100),2)
    player2_perc = round(((player2_wins / numgames)* 100),2)
    draw_perc = round(((draws / numgames) * 100),3)
    
    print (f"Player 1 wins: {player1_perc}%")
    print (f"Player 2 wins: {player2_perc}%")
    print (f"Ties: {draw_perc}%")

if __name__ == "__main__":
    main()

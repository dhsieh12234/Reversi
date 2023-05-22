"""
Bots for Reversi
(and command for running simulations with bots)
"""

import random
import sys
from typing import Union, Tuple, Optional, List
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

    def __init__(self, reversi: ReversiBase):
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

    def __init__(self, reversi: ReversiBase):
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

    def suggest_move_v2(self) -> int:

        def num_squares(grid: Reversi) -> int:
            """
            Checks to see how many pieces a specific players has on the
            board

            Inputs:
                grid: the current grid after making the move
            
            Returns: the number of pieces a player has
            """
            count = 0
            for row in grid._board.grid:
                for square in row:
                    if square == self._reversi.turn:
                        count += 1
            return count

        moves = self._reversi.available_moves
        optimal_move = moves[0]
        num_square = 0
        for move in moves:
            new_grid = self._reversi.simulate_moves([move])
            count = num_squares(new_grid)
            if count > num_square:
                optimal_move = move
                num_square = count
        return optimal_move

class VerySmartBot:
    """
    Simple Bot that just picks a move at random
    """

    _reversi: Reversi

    def __init__(self, reversi: ReversiBase):
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

        #OLD CODE:
        """
        # loops thru the avaliable moves by P1
        count = self._reversi._side ** 2
        moves = self._reversi.available_moves
        optimal_move = [moves[0]]
        for move1 in moves:
            new_grid: Reversi = self._reversi.simulate_moves([move1])
            moves2 = new_grid.available_moves
            captured_pieces = []

        #  get the average for the moves avaliable for P2
            for move2 in moves2:
                captured_pieces.append(len(new_grid.captures(move2)))
            # print(f"all captured pieces: {captured_pieces}")
            average = find_average(captured_pieces)
            # print(f"average: {average}")
        
        # compare average of 1 move to the other
            if average < count:
                count = average
                optimal_move = []
                optimal_move.append(move1)
            elif average == count:
                optimal_move.append(move1)
        return random.choice(optimal_move)
        """

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

    
def play_game(bot1: str, bot2: str, game: Reversi) \
                                                            -> list[int]:
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
        # print("\n")
        # print("NEW TURN")
        if game.turn == 1:
            game_bot.move(bot1)
            # print(f"player 1 move: {move}")
        elif game.turn == 2:
            game_bot.move(bot2)
            # print(f"player 2 move: {move}")
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
        result = play_game("random", "smart", Reversi(8, 2, True))
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


def main():
    startTime = time.time()
    numgame = int(sys.argv[1])
    play_num_games(numgame)
    endTime = time.time()
    elapsedTime = endTime - startTime
    print(f'time={elapsedTime:6.3f}')

if __name__ == "__main__":
    main()

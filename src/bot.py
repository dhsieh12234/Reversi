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
    _player1: Piece

    def __init__(self, reversi: ReversiBase, player1: Piece):
        """ Constructor

        Args:
            board: Board the bot will play on
            player1: bot player
            player2: opposing player
        """
        self._reversi = reversi
        self._player1 = player1

    def suggest_move(self) -> int:
        """ Suggests a move

        Returns: None

        """
        moves = self._reversi.available_moves
        print(f"random moves: {moves}")
        if len(moves) == 0:
            return None
        return random.choice(moves)

class SmartBot:
    """
    Smart bot that chooses move based off amount of captured pieces
    """

    _reversi: Reversi
    _player1: Piece

    def __init__(self, reversi: ReversiBase, player1: Piece):
        """ Constructor

        Args:
            board: Board the bot will play on
            player1: bot player
            player2: opposing player
        """
        self._reversi = reversi
        self._player1 = player1

    def suggest_move(self) -> int:
        """ Suggests a move

        Returns: None

        """
        def in_board(pos: Tuple[int, int]) -> bool:
            """
            Checks whether a move can be placed onto the board

            Inputs:
                pos: the position of a piece
            
            Returns: True, if the piece is in the board.
                False, if the piece is outside the board
            """
            i, j = pos
            return ((i >= 0) and (i < self._reversi._side)\
                            and (j >= 0) and (j < self._reversi._side))

        moves = self._reversi.available_moves
        optimal_move = [moves[0]]
        max_captured_pieces = 0
        for move in moves:
            print(f"tested move: {move}")
            x,y = move
            cur_captured_pieces_count = 0
            directions: List[Tuple[int, int]] = [(0, 1), (-1, 1), (-1, 0), \
                (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1)]
            for d in directions:
                k,l = d
                captured_pieces: List[Tuple[int, int]] = []
                n: int = 1
                while in_board((x + n * k, y + n * l)):
                    if n == 1 and self._reversi._board.grid[x + n * k][y + n * l] == self._player1:
                        break
                    if self._reversi._board.grid[x + n * k][y + n * l] is None:
                        break
                    if self._reversi._board.grid[x + n * k][y + n * l] == self._player1:
                        cur_captured_pieces_count += len(captured_pieces)
                        break
                    captured_pieces.append((x + n * k, y + n * l))
                    n += 1
                continue
            print(f"number captured pieces: {cur_captured_pieces_count}")
            if cur_captured_pieces_count > max_captured_pieces:
                max_captured_pieces = cur_captured_pieces_count
                optimal_move = []
                optimal_move = [move]
            elif cur_captured_pieces_count == max_captured_pieces:
                optimal_move.append(move)
        return random.choice(optimal_move)

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
    _player1: Piece

    def __init__(self, reversi: ReversiBase, player1: Piece):
        """ Constructor

        Args:
            board: Board the bot will play on
            player1: bot player
            player2: opposing player
        """
        self._reversi = reversi
        self._player1 = player1


    def suggest_move(self) -> int:
        """ Suggests a move

        Returns: None

        """
      
        def num_captured_pieces(move, grid):
            print (f"tested move: {move}")
            x,y = move
            directions: List[Tuple[int, int]] = [(0, 1), (-1, 1), (-1, 0), \
                (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1)]
            captured_pieces = []
            for d in directions:
                k,l = d
                n: int = 1
                while in_board((x + n * k, y + n * l)):
                    if n == 1 and grid[x + n * k][y + n * l] == self._reversi.turn:
                        break
                    if grid[x + n * k][y + n * l] is None:
                        break
                    if grid[x + n * k][y + n * l] == self._reversi.turn:
                        break
                    captured_pieces.append((x + n * k, y + n * l))
                    n += 1
                continue
            print(f"captured pieces: {captured_pieces}")
            return len(captured_pieces)

        def in_board(pos: Tuple[int, int]) -> bool:
            """
            Checks whether a move can be placed onto the board

        Inputs:
                pos: the position of a piece
            
            Returns: True, if the piece is in the board.
                False, if the piece is outside the board
            """
            i, j = pos
            return ((i >= 0) and (i < self._reversi._side)\
                         and (j >= 0) and (j < self._reversi._side))    
        
        def find_average (list):
            sum = 0
            for num in list:
                sum += num
            return sum / (len(list))


        # loops thru the avaliable moves by P1
        count = self._reversi._side ** 2
        moves = self._reversi.available_moves
        optimal_move = [moves[0]]
        for move1 in moves:
            new_grid = self._reversi.simulate_moves([move1])
            moves2 = new_grid.available_moves
            captured_pieces = []

        #  get the average for the moves avaliable for P2
            for move2 in moves2:
                captured_pieces.append(num_captured_pieces(move2, new_grid.grid))
            print(f"all captured pieces: {captured_pieces}")
            average = find_average(captured_pieces)
            print(f"average: {average}")
        
        # compare average of 1 move to the other
            if average < count:
                count = average
                optimal_move = []
                optimal_move.append(move1)
            elif average == count:
                optimal_move.append(move1)
        return random.choice(optimal_move)

class ReversiBot:
    """
    Gets a random for the bot to act upon
    """

    def __init__(self, player: int, reversi: Reversi) -> None:
        """
        Constructor

        Args: 
            player: the player whos moves you are finding
            stub: the grid of the current game
        """
        self.player = player
        if self.player == "random":
            # print("Random Bot")
            self.bot = RandomBot(reversi, player)
        elif self.player == "smart":
            # print("Smart Bot")
            self.bot = SmartBot(reversi, player)
        elif self.player == "very smart":
            # print("Very Smart Bot")
            self.bot = VerySmartBot(reversi, player)

    
def play_game(player1: ReversiBot, player2: ReversiBot, game: Reversi) \
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

    while not (len(game.outcome) == 1 or len(game.outcome) == 2):
        print("\n")
        print("NEW TURN")
        if game.turn == 1:
            move = player1.bot.suggest_move()
            print(f"player 1 move: {move}")
            if move is not None:
                game.apply_move(move)
        elif game.turn == 2:
            move = player2.bot.suggest_move()
            print(f"player 2 move: {move}")
            if move is not None:
                game.apply_move(move)
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
        board = Reversi (8,2, True)
        player1 = ReversiBot("random", board)
        player2 = ReversiBot("very smart", board)
        result = play_game(player1, player2, board)
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
main()

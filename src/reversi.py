"""
Reversi implementation.
Contains a base class (ReversiBase). You must implement
a Reversi class that inherits from this base class.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Reversible, Tuple, Optional
from copy import deepcopy

BoardGridType = List[List[Optional[int]]]
"""
Type for representing the state of the game board (the "grid")
as a list of lists. Each entry will either be an integer (meaning
there is a piece at that location for that player) or None,
meaning there is no piece in that location. Players are
numbered from 1.
"""

ListMovesType = List[Tuple[int, int]]
"""
Type for representing lists of moves on the board.
"""


class ReversiBase(ABC):
    """
    Abstract base class for the game of Reversi
    """

    _side: int
    _players: int
    _othello: bool

    def __init__(self, side: int, players: int, othello: bool):
        """
        Constructor
        Args:
            side: Number of squares on each side of the board
            players: Number of players
            othello: Whether to initialize the board with an Othello
            configuration.
        Raises:
            ValueError: If the parity of side and players is incorrect
        """
        self._side = side
        self._players = players
        self._othello = othello

    #
    # PROPERTIES
    #

    @property
    def size(self) -> int:
        """
        Returns the size of the board (the number of squares per side)
        """
        return self._side

    @property
    def num_players(self) -> int:
        """
        Returns the number of players
        """
        return self._players

    @property
    @abstractmethod
    def grid(self) -> BoardGridType:
        """
        Returns the state of the game board as a list of lists.
        Each entry can either be an integer (meaning there is a
        piece at that location for that player) or None,
        meaning there is no piece in that location. Players are
        numbered from 1.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def turn(self) -> int:
        """
        Returns the player number for the player who must make
        the next move (i.e., "whose turn is it?")  Players are
        numbered from 1.
        If the game is over, this property will not return
        any meaningful value.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def available_moves(self) -> ListMovesType:
        """
        Returns the list of positions where the current player
        (as returned by the turn method) could place a piece.
        If the game is over, this property will not return
        any meaningful value.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def done(self) -> bool:
        """
        Returns True if the game is over, False otherwise.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def outcome(self) -> List[int]:
        """
        Returns the list of winners for the game. If the game
        is not yet done, will return an empty list.
        If the game is done, will return a list of player numbers
        (players are numbered from 1). If there is a single winner,
        the list will contain a single integer. If there is a tie,
        the list will contain more than one integer (representing
        the players who tied)
        """
        raise NotImplementedError

    #
    # METHODS
    #

    @abstractmethod
    def piece_at(self, pos: Tuple[int, int]) -> Optional[int]:
        """
        Returns the piece at a given location
        Args:
            pos: Position on the board
        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.
        Returns: If there is a piece at the specified location,
        return the number of the player (players are numbered
        from 1). Otherwise, return None.
        """
        raise NotImplementedError

    @abstractmethod
    def legal_move(self, pos: Tuple[int, int]) -> bool:
        """
        Checks if a move is legal.
        Args:
            pos: Position on the board
        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.
        Returns: If the current player (as returned by the turn
        method) could place a piece in the specified position,
        return True. Otherwise, return False.
        """
        raise NotImplementedError

    @abstractmethod
    def apply_move(self, pos: Tuple[int, int]) -> None:
        """
        Place a piece of the current player (as returned
        by the turn method) on the board.
        The provided position is assumed to be a legal
        move (as returned by available_moves, or checked
        by legal_move). The behaviour of this method
        when the position is on the board, but is not
        a legal move, is undefined.
        After applying the move, the turn is updated to the
        next player who can make a move. For example, in a 4
        player game, suppose it is player 1's turn, they
        apply a move, and players 2 and 3 have no possible
        moves, but player 4 does. After player 1's move,
        the turn would be set to 4 (not to 2).
        If, after applying the move, none of the players
        can make a move, the game is over, and the value
        of the turn becomes moot. It cannot be assumed to
        take any meaningful value.
        Args:
            pos: Position on the board
        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.
        Returns: None
        """
        raise NotImplementedError

    @abstractmethod
    def load_game(self, turn: int, grid: BoardGridType) -> None:
        """
        Loads the state of a game, replacing the current
        state of the game.
        Args:
            turn: The player number of the player that
            would make the next move ("whose turn is it?")
            Players are numbered from 1.
            grid: The state of the board as a list of lists
            (same as returned by the grid property)
        Raises:
             ValueError:
             - If the value of turn is inconsistent
               with the _players attribute.
             - If the size of the grid is inconsistent
               with the _side attribute.
             - If any value in the grid is inconsistent
               with the _players attribute.
        Returns: None
        """
        raise NotImplementedError

    @abstractmethod
    def simulate_moves(self,
                       moves: ListMovesType
                       ) -> "ReversiBase":
        """
        Simulates the effect of making a sequence of moves,
        **without** altering the state of the game (instead,
        returns a new object with the result of applying
        the provided moves).
        The provided positions are assumed to be legal
        moves. The behaviour of this method when a
        position is on the board, but is not a legal
        move, is undefined.
        Bear in mind that the number of *turns* involved
        might be larger than the number of moves provided,
        because a player might not be able to make a
        move (in which case, we skip over the player).
        Let's say we provide moves (2,3), (3,2), and (1,2)
        in a 3 player game, that it is player 2's turn,
        and that Player 3 won't be able to make any moves.
        The moves would be processed like this:
        - Player 2 makes move (2, 3)
        - Player 3 can't make any moves
        - Player 1 makes move (3, 2)
        - Player 2 makes move (1, 2)
        Args:
            moves: List of positions, representing moves.
        Raises:
            ValueError: If any of the specified positions
            is outside the bounds of the board.
        Returns: An object of the same type as the object
        the method was called on, reflecting the state
        of the game after applying the provided moves.
        """
        raise NotImplementedError

class Piece:
    """
    Class to represent pieces.
    """

    name: int

    def __init__(self, name: int):
        self.name = name

    def __str__(self) -> str:
        """
        Returns: a string representation of the piece.
        """
        return str(self.name)

PieceBoardType = List[List[Optional[Piece]]]

class Board:
    """
    Class to represent a game board.
    """

    grid: PieceBoardType

    def __init__(self, grid: BoardGridType):
        n: int = len(grid)
        self.grid = [[None] * n for _ in range(n)]
        for i, row in enumerate(grid):
            for j, square in enumerate(row):
                if square is not None:
                    self.grid[i][j] = Piece(square)


    def in_board(self, pos: Tuple[int, int]) -> bool:
        """
        Returns whether pos is in the board or not.
        Args:
            pos: Position on the board
        Returns: whether or not pos is on the board
        """
        i, j = pos
        n = len(self.grid)
        return ((i >= 0) and (i < n) and (j >= 0) and (j < n))

    def __str__(self) -> str:
        """
        Returns: String representation of the board
        """
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

        #first construct an empty grid to fill in
        n: int = 2 * len(self.grid) + 1
        str_grid: List[List[str]] = [[" "] * n for _ in range(n)]

        #fill in the grid
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
                else:
                    i = (k - 1) // 2
                    j = (l - 1) // 2
                    if not self.grid[i][j] is None:
                        str_grid[k][l] = str(self.grid[i][j])

        #turn str_grid into a string
        rv: List[str] = [""] * n
        for k, grid_row in enumerate(str_grid):
            rv[k] = "".join(grid_row)
        return "\n".join(rv)


class Reversi(ReversiBase):
    """
    Class to represent a Reversi game.
    """

    _side: int
    _players: int
    _othello: bool
    _board: Board
    _total_turns: int
    _done: bool

    def __init__(self, side: int, players: int, othello: bool):
        """
        Constructor
        Args:
            side: Number of squares on each side of the board
            players: Number of players
            othello: Whether to initialize the board with an Othello
            configuration.
        Raises:
            ValueError: If the parity of side and players is incorrect
        """
        if players > 9 or players < 2:
            raise ValueError("The number of players must be between 2 and 9 " +
                             "inclusive.")
        if players % 2 != side % 2:
            raise ValueError("The number of players and side length must " +
                             "have the same parity.")
        if othello and players != 2:
            raise ValueError("The Othello variant can only be played with 2 " +
                             "players.")
        if side < 3:
            raise ValueError("The side length must be at least 3.")
        super().__init__(side, players, othello)
        self._board = Board([[None] * side for _ in range(side)])
        self._total_turns = 0
        if othello:
            self._board.grid[side // 2][side // 2 - 1] = Piece(1)
            self._board.grid[side // 2 - 1][side // 2] = Piece(1)
            self._board.grid[side // 2 - 1][side // 2 - 1] = Piece(2)
            self._board.grid[side // 2][side // 2] = Piece(2)
        self._done = False
    #
    # PROPERTIES
    #

    @property
    def grid(self) -> BoardGridType:
        """
        Returns the state of the game board as a list of lists.
        Each entry can either be an integer (meaning there is a
        piece at that location for that player) or None,
        meaning there is no piece in that location. Players are
        numbered from 1.
        """
        grid: BoardGridType = [[None] * self._side for _ in range(self._side)]
        for i, row in enumerate(self._board.grid):
            for j, square in enumerate(row):
                if not square is None:
                    grid[i][j] = square.name
        return grid

    @property
    def turn(self) -> int:
        """
        Returns the player number for the player who must make
        the next move (i.e., "whose turn is it?")  Players are
        numbered from 1.
        If the game is over, this property will not return
        any meaningful value.
        """
        return self._total_turns % self._players + 1

    @property
    def available_moves(self) -> ListMovesType:
        """
        Returns the list of positions where the current player
        (as returned by the turn method) could place a piece.
        If the game is over, this property will not return
        any meaningful value.
        """
        if self.done:
            return [(-1, -1)]
        else:
            avail_moves: List = []
            for x, j in enumerate(self._board.grid):
                for y, k in enumerate(j):
                    if self.legal_move((x, y)):
                        avail_moves.append((x, y))
            return avail_moves


    @property
    def done(self) -> bool:
        """
        Returns True if the game is over, False otherwise.
        """
        return self._done

    @property
    def outcome(self) -> List[int]:
        """
        Returns the list of winners for the game. If the game
        is not yet done, will return an empty list.
        If the game is done, will return a list of player numbers
        (players are numbered from 1). If there is a single winner,
        the list will contain a single integer. If there is a tie,
        the list will contain more than one integer (representing
        the players who tied)
        """
        if not self.done:
            return []
        winners: List[int] = []
        piece_count: List[int] = [0] * self._players
        for row in self.grid:
            for square in row:
                if square is not None:
                    piece_count[square - 1] += 1
        for i, count in enumerate(piece_count):
            if count == max(piece_count):
                winners.append(i + 1)
        print(piece_count)
        return winners

    #
    # METHODS
    #

    def piece_at(self, pos: Tuple[int, int]) -> Optional[int]:
        """
        Returns the piece at a given location
        Args:
            pos: Position on the board
        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.
        Returns: If there is a piece at the specified location,
        return the number of the player (players are numbered
        from 1). Otherwise, return None.
        """
        if not self._board.in_board(pos):
            raise ValueError("The specified position is outside the bounds" +
                             "of the board.")
        i, j = pos
        return self.grid[i][j]

    def legal_move(self, pos: Tuple[int, int]) -> bool:
        """
        Checks if a move is legal.
        Args:
            pos: Position on the board
        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.
        Returns: If the current player (as returned by the turn
        method) could place a piece in the specified position,
        return True. Otherwise, return False.
        """
        i, j = pos
        if self.piece_at(pos) is not None:
            return False

        prelim: bool = False
        n: int = (self._side - self._players) // 2
        inner_square_indices: List[int] = list(range(n, self._side - n))
        for x in inner_square_indices:
            for y in inner_square_indices:
                prelim = prelim or (self._board.grid[x][y] is None)
        if prelim:
            return (i in inner_square_indices) and (j in inner_square_indices)

        directions: List[Tuple[int, int]] \
            = [(0, 1), (-1, 1), (-1, 0), (-1, -1), \
               (0, -1), (1, -1), (1, 0), (1, 1)]

        for d in directions:
            k, l = d
            m: int = 1
            while self._board.in_board((i + m * k, j + m * l)):
                if m == 1 and self.grid[i + m * k][j + m * l] == self.turn:
                    break
                if self.grid[i + m * k][j + m * l] is None:
                    break
                if self.grid[i + m * k][j + m * l] == self.turn:
                    return True
                m += 1
            continue
        return False

    def apply_move(self, pos: Tuple[int, int]) -> None:
        """
        Place a piece of the current player (as returned
        by the turn method) on the board.
        The provided position is assumed to be a legal
        move (as returned by available_moves, or checked
        by legal_move). The behaviour of this method
        when the position is on the board, but is not
        a legal move, is undefined.
        After applying the move, the turn is updated to the
        next player who can make a move. For example, in a 4
        player game, suppose it is player 1's turn, they
        apply a move, and players 2 and 3 have no possible
        moves, but player 4 does. After player 1's move,
        the turn would be set to 4 (not to 2).
        If, after applying the move, none of the players
        can make a move, the game is over, and the value
        of the turn becomes moot. It cannot be assumed to
        take any meaningful value.
        Args:
            pos: Position on the board
        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.
        Returns: None
        """
        if not self._board.in_board(pos):
            raise ValueError("The specified position is outside the bounds" +
                             "of the board.")
        i, j = pos
        self._board.grid[i][j] = Piece(self.turn)
        
        n: int = (self._side - self._players) // 2
        inner_square_indices: List[int] = list(range(n, self._side - n))
        prelim: bool = (i in inner_square_indices) \
            and (j in inner_square_indices)
        

        directions: List[Tuple[int, int]] \
            = [(0, 1), (-1, 1), (-1, 0), (-1, -1), \
               (0, -1), (1, -1), (1, 0), (1, 1)]

        #captures
        if not prelim:
            for d in directions:
                k, l = d
                captured_pieces: List[Tuple[int, int]] = []
                n = 1
                while self._board.in_board((i + n * k, j + n * l)):
                    if n == 1 and self.grid[i + n * k][j + n * l] == self.turn:
                        break
                    if self.grid[i + n * k][j + n * l] is None:
                        break
                    if self.grid[i + n * k][j + n * l] == self.turn:
                        for x, y in captured_pieces:
                            self._board.grid[x][y] = Piece(self.turn)
                        break
                    captured_pieces.append((i + n * k, j + n * l))
                    n += 1
                continue

        #update turns and check if done
        self._total_turns += 1
        next_player = self.turn
        while self.available_moves == []:
            self._total_turns += 1
            if self.turn == next_player:
                self._done = True
                break
        print(self._board)


    def load_game(self, turn: int, grid: BoardGridType) -> None:
        """
        Loads the state of a game, replacing the current
        state of the game.
        Args:
            turn: The player number of the player that
            would make the next move ("whose turn is it?")
            Players are numbered from 1.
            grid: The state of the board as a list of lists
            (same as returned by the grid property)
        Raises:
             ValueError:
             - If the value of turn is inconsistent
               with the _players attribute.
             - If the size of the grid is inconsistent
               with the _side attribute.
             - If any value in the grid is inconsistent
               with the _players attribute.
        Returns: None
        """
        if turn < 1 or turn > self._players:
            raise ValueError("The value of turn is inconsistent with the " +
                             "number of players.")

        if len(grid) != self._side:
            raise ValueError("The size of the grid is inconsistent with the " +
                             "size property.")
        legal_entries: List[Optional[int]] = [None] + \
            list(range(1, self._players + 1))
        for row in grid:
            for square in row:
                if square not in legal_entries:
                    raise ValueError("The values in the grid are " +
                                     "inconsistent with the number of players.")
        self._total_turns = turn - 1
        self._board = Board(grid)

        #check if the loaded game is done
        sim_game: Reversi = deepcopy(self)
        sim_game._total_turns += 1
        next_player = sim_game.turn
        while sim_game.available_moves == []:
            sim_game._total_turns += 1
            if sim_game.turn == next_player:
                sim_game._done = True
                break


    def simulate_moves(self,
                       moves: ListMovesType
                       ) -> "ReversiBase":
        """
        Simulates the effect of making a sequence of moves,
        **without** altering the state of the game (instead,
        returns a new object with the result of applying
        the provided moves).
        The provided positions are assumed to be legal
        moves. The behaviour of this method when a
        position is on the board, but is not a legal
        move, is undefined.
        Bear in mind that the number of *turns* involved
        might be larger than the number of moves provided,
        because a player might not be able to make a
        move (in which case, we skip over the player).
        Let's say we provide moves (2,3), (3,2), and (1,2)
        in a 3 player game, that it is player 2's turn,
        and that Player 3 won't be able to make any moves.
        The moves would be processed like this:
        - Player 2 makes move (2, 3)
        - Player 3 can't make any moves
        - Player 1 makes move (3, 2)
        - Player 2 makes move (1, 2)
        Args:
            moves: List of positions, representing moves.
        Raises:
            ValueError: If any of the specified positions
            is outside the bounds of the board.
        Returns: An object of the same type as the object
        the method was called on, reflecting the state
        of the game after applying the provided moves.
        """
        sim_game: Reversi = deepcopy(self)
        for i, move in enumerate(moves):
            if sim_game.done:
                # print(f"The game ended at move {i}.")
                return sim_game
            if not self._board.in_board(move):
                raise ValueError("All moves must be on the board.")
            sim_game.apply_move(move)
        return sim_game

    def __str__(self):
        return str(self._board)

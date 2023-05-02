"""
Mock implementations of ReversiBase.

We provide a ReversiStub implementation, and you must
implement a ReversiMock implementation.
"""
from typing import List, Tuple, Optional
from copy import deepcopy

from reversi import ReversiBase, BoardGridType, ListMovesType


class ReversiStub(ReversiBase):
    """
    Stub implementation of ReversiBase.

    This stub implementation behaves according to the following rules:

    - It only supports two players and boards of size 2x2 and above.
    - The board is always initialized with four pieces in the four corners
      of the board. Player 1 has pieces in the northeast and southwest
      corners of the board, and Player 2 has pieces in the southeast and
      northwest corners of the board.
    - All moves are legal, even if there is already a piece in a given position.
    - The game ends after four moves. Whatever player has a piece in position
      (0,1) wins. If there is no piece in that position, the game ends in a tie.
    - It does not validate board positions. If a method
      is called with a position outside the board, the method will likely cause
      an exception.
    - It does not implement the ``load_game`` or ``simulate_moves`` method.
    """

    _grid: BoardGridType
    _turn: int
    _num_moves: int

    def __init__(self, side: int, players: int, othello: bool):
        if players != 2:
            raise ValueError("The stub implementation "
                             "only supports two players")

        super().__init__(side, players, othello)

        self._grid = [[None]*side for _ in range(side)]
        self._grid[0][-1] = 1
        self._grid[-1][0] = 1
        self._grid[0][0] = 2
        self._grid[-1][-1] = 2

        self._turn = 1
        self._num_moves = 0

    @property
    def grid(self) -> BoardGridType:
        return deepcopy(self._grid)

    @property
    def turn(self) -> int:
        return self._turn

    @property
    def available_moves(self) -> ListMovesType:
        moves = []
        for r in range(self._side):
            for c in range(self._side):
                moves.append((r, c))

        return moves

    @property
    def done(self) -> bool:
        return self._num_moves == 4

    @property
    def outcome(self) -> List[int]:
        if not self.done:
            return []

        if self._grid[0][1] is None:
            return [0, 1]
        else:
            return [self._grid[0][1]]

    def piece_at(self, pos: Tuple[int, int]) -> Optional[int]:
        r, c = pos
        return self._grid[r][c]

    def legal_move(self, pos: Tuple[int, int]) -> bool:
        return True

    def apply_move(self, pos: Tuple[int, int]) -> None:
        r, c = pos
        self._grid[r][c] = self._turn
        self._turn = 2 if self._turn == 1 else 1
        self._num_moves += 1

    def load_game(self, turn: int, grid: BoardGridType) -> None:
        raise NotImplementedError()

    def simulate_moves(self,
                       moves: ListMovesType
                       ) -> ReversiBase:
        raise NotImplementedError()

class ReversiMock(ReversiBase):
    """

    """
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
        if players != 2:
            raise ValueError("There can only be 2 players.")
        if side < 4:
            raise ValueError("The board can be no smaller than 4x4.")
        if side % players != 0:
            raise ValueError("The board side length must be divisible by the \
                             number of players.")
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
    def available_moves(self) -> ListMovesType:
        """
        Returns the list of positions where the current player
        (as returned by the turn method) could place a piece.

        If the game is over, this property will not return
        any meaningful value.
        """
        raise NotImplementedError

    @property
    def done(self) -> bool:
        """
        Returns True if the game is over, False otherwise.
        """
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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



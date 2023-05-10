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
    Mock Reversi class.
    """

    _side: int
    _players: int
    _othello: bool
    _grid: BoardGridType
    num_moves: int

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
        self._grid = [[None] * side for _ in range(side)]
        if othello:
            self._grid[side // 2][side // 2 - 1] = 1
            self._grid[side // 2 - 1][side // 2] = 1
            self._grid[side // 2 - 1][side // 2 - 1] = 2
            self._grid[side // 2][side // 2] = 2
        self.num_moves = 0

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
        return deepcopy(self._grid)

    @property
    def turn(self) -> int:
        """
        Returns the player number for the player who must make
        the next move (i.e., "whose turn is it?")  Players are
        numbered from 1.

        If the game is over, this property will not return
        any meaningful value.
        """
        if self.done:
            return -1
        else:
            return self.num_moves % self.num_players + 1

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
            for x, j in enumerate(self.grid):
                for y, k in enumerate(j):
                    if self.legal_move((x, y)):
                        avail_moves.append((x, y))
            return avail_moves

    @property
    def done(self) -> bool:
        """
        Returns True if the game is over, False otherwise.
        """
        return not ((self._grid[0][0] is None) and (self._grid[-1][-1] is None))

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
        ret_lst: List = []
        if not self.done:
            return ret_lst
        else:
            if self._grid[0][0] is not None: 
                ret_lst.append(self._grid[0][0])
            else:
                count: int = 0
                for players in range(self.num_players):
                    count = count + 1
                    ret_lst.append(count)
            return ret_lst


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
        x, y = pos
        if x >= self._side or y >= self._side:
            raise ValueError("Specified position is outside the bounds.")
        return self._grid[x][y]

    
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
        def in_board(pos: Tuple[int, int]) -> bool:
            i, j = pos
            return ((i >= 0) and (i < self._side)\
                         and (j >= 0) and (j < self._side))
        if not in_board(pos):
            raise ValueError("The specified position is outside the bounds \
                             of the board.")
        i, j = pos
        if self.grid[i][j] is not None:
            return False
        if pos == (0, 0) or pos == (self._side - 1, self._side - 1):
            return True
        
        directions: List[Tuple[int, int]] = [(0, 1), (-1, 1), (-1, 0), (-1, -1), \
                      (0, -1), (1, -1), (1, 0), (1, 1)]

        for d in directions:
            k, l = d
            if in_board((i + k, j + l)):
                if self.grid[i + k][j + l] is not None:
                    return True
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
        x, y = pos
        if x >= self._side or x < 0 or y >= self._side or y < 0:
            raise ValueError("Specified position is outside the bounds.")
        self._grid[x][y] = self.turn
        self.num_moves += 1
        

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
        sim_game: ReversiMock = deepcopy(self)
        sim_game.apply_move(moves[0])
        return sim_game

class ReversiBotMock(ReversiMock):
    """
    Mock Reversi Bot class.
    """

    _side: int
    _players: int
    _othello: bool
    _grid: BoardGridType
    num_moves: int

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
        self._grid = [[None] * side for _ in range(side)]
        if othello:
            self._grid[side // 2][side // 2 - 1] = 1
            self._grid[side // 2 - 1][side // 2] = 1
            self._grid[side // 2 - 1][side // 2 - 1] = 2
            self._grid[side // 2][side // 2] = 2
        self.num_moves = 0

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
        return deepcopy(self._grid)

    @property
    def turn(self) -> int:
        """
        Returns the player number for the player who must make
        the next move (i.e., "whose turn is it?")  Players are
        numbered from 1.

        If the game is over, this property will not return
        any meaningful value.
        """
        if self.done:
            return -1
        else:
            return self.num_moves % self.num_players + 1

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
            for x, j in enumerate(self.grid):
                for y, k in enumerate(j):
                    if self.legal_move((x, y)):
                        avail_moves.append((x, y))
            return avail_moves

    @property
    def done(self) -> bool:
        """
        Returns True if the game is over, False otherwise.
        """
        for row in self.grid:
            for square in row:
                if square is None:
                    return False
        return True 

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
        else:
            player1 = 0
            player2 = 0 
            for row in self.grid:
                for square in row:
                    if square == 1:
                        player1 += 1
                    if square == 2:
                        player2 += 1
            if player1 > player2:
                return [1]
            if player2 < player1:
                return [2]
            if player1 == player2:
                return [1,2]

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
        x, y = pos
        if x >= self._side or y >= self._side:
            raise ValueError("Specified position is outside the bounds.")
        return self._grid[x][y]

    
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
        def in_board(pos: Tuple[int, int]) -> bool:
            i, j = pos
            return ((i >= 0) and (i < self._side)\
                         and (j >= 0) and (j < self._side))
        if not in_board(pos):
            raise ValueError("The specified position is outside the bounds \
                             of the board.")
        i, j = pos
        if self.grid[i][j] is not None:
            return False
        
        directions: List[Tuple[int, int]] = [(0, 1), (-1, 1), (-1, 0), (-1, -1), \
                      (0, -1), (1, -1), (1, 0), (1, 1)]

        for d in directions:
            k, l = d
            if in_board((i + k, j + l)):
                if self.grid[i + k][j + l] is not None:
                    return True
            if pos == (0, 0) or pos == (self._side - 1, self._side - 1):
                return True
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
        def in_board(pos: Tuple[int, int]) -> bool:
            i, j = pos
            return ((i >= 0) and (i < self._side)\
                         and (j >= 0) and (j < self._side))
        x, y = pos
        if x >= self._side or x < 0 or y >= self._side or y < 0:
            raise ValueError("Specified position is outside the bounds.")
        self._grid[x][y] = self.turn
        
        directions: List[Tuple[int, int]] = [(0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1)]

        for d in directions:
            k,l = d
            captured_pieces: List[Tuple[int, int]] = []
            n: int = 1
            while in_board((x + n * k, y + n * l)):
                if n == 1 and self.grid[x + n * k][y + n * l] == self.turn:
                    break
                if self.grid[x + n * k][y + n * l] is None:
                    break
                if self.grid[x + n * k][y + n * l] == self.turn:
                    for a, b in captured_pieces:
                        self.grid[a][b] = self.turn
                    break
                captured_pieces.append((x + n * k, y + n * l))
                n += 1
            continue
        print (self.grid)

       
        self.num_moves += 1
        next_player = self.turn
        while self.available_moves == []:
            self.num_moves += 1
            if self.turn == next_player:
                self._done = True
                break



        

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
        sim_game: ReversiBotMock = deepcopy(self)
        sim_game.apply_move(moves)
        # print (f"printed simulated game: {sim_game}")
        return sim_game


    
    def choose_move(self):

        def num_squares(grid: ReversiBotMock):
            count = 0
            for row in grid.grid:
                for square in row:
                    if square == self.turn:
                        count += 1
            return count


        moves = self.available_moves
        print (f"avaliable moves: {moves}")
        optimal_move = moves[0]
        print (f"mock optimal move: {optimal_move}")
        num_square = 0
        for move in moves:
            new_grid = self.simulate_moves(move)
            count = num_squares(new_grid)
            # print (f"new grid: {new_grid}")
            if count > num_square:
                optimal_move = move
                num_square = count
        return optimal_move
    


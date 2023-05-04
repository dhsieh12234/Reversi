
from reversi import Reversi, ReversiBase


def test_size_1():
    """
    Testing the size of the Othello Board 3x3 without configuration
    """
    game = Reversi(side=3, players=2, othello=False)
    assert len(game.grid) == 3
    for x, cols in enumerate(game.grid):
        assert len(cols) == 3
        for y, vals in enumerate(cols):
            assert vals == None, f"Expected grid[{x}][{y}] to be None but got {vals}"


def test_size_2():
    """
    Testing the size of the Othello Board 4x4 without configuration
    """
    game = Reversi(side=4, players=2, othello=False)
    assert len(game.grid) == 4
    for x, cols in enumerate(game.grid):
        assert len(cols) == 4
        for y, vals in enumerate(cols):
            assert vals == None, f"Expected grid[{x}][{y}] to be None but got {vals}"

def test_size_3():
    """
    Testing the size of the Othello Board 4x4 with configuration
    Black = Player 1
    White = Player 2
    """
    game = Reversi(side=4, players=2, othello=True)
    assert game.grid[1][2] == 1 and game.grid[2][1] == 1
    assert game.grid[1][1] == 2 and game.grid[2][2] == 2
    for i, cols in enumerate(game.grid):
        for i, vals in enumerate(game.grid):
            if i == 1:
                if i != 2 or 1:
                    assert vals == None
            if i == 2:
                if i != 2 or 1:
                    assert vals == None
            else:
                assert vals == None

def test_size_4():
    """
    Testing the size of the Othello Board 5x5 without configuration
    """
    game = Reversi(side=5, players=3, othello=False)
    assert len(game.grid) == 5
    for x, cols in enumerate(game.grid):
        assert len(cols) == 5
        for y, vals in enumerate(cols):
            assert vals == None, f"Expected grid[{x}][{y}] to be None but got {vals}"


def test_size_5():
    """
    Testing the size of the Othello Board 6x6 without configuration
    """
    game = Reversi(side=6, players=2, othello=True)
    assert len(game.grid) == 6
    assert game.grid[3][3] == 2 and game.grid[2][2] == 2
    assert game.grid[3][2] == 1 and game.grid[2][3] == 1
    for x, cols in enumerate(game.grid):
        assert len(cols) == 6
        for y, vals in enumerate(game.grid):
            if x == 2:
                if y != 2 or 3:
                    assert vals == None, f"Expected grid[{x}][{y}] to be None but got {vals}"
            if x == 3:
                if y != 3 or 2:
                    assert vals == None, f"Expected grid[{x}][{y}] to be None but got {vals}"
            else:
                assert vals == None, f"Expected grid[{x}][{y}] to be None but got {vals}"

def test_size_6():
    """
    Testing the size of the Othello Board 7x7 without configuration
    """
    game = Reversi(side=7, players=3, othello=False)
    assert len(game.grid) == 7
    for x, cols in enumerate(game.grid):
        assert len(cols) == 7
        for y, vals in enumerate(cols):
            assert vals == None, f"Expected grid[{x}][{y}] to be None but got {vals}"

def test_size_7():
    """
    Testing the size of the Board 20x20 with configuration
    """
    game = Reversi(side=20, players=10, othello=False)

    assert len(game.grid) == 20
    for x, cols in enumerate(game.grid):
        assert len(cols) == 20
        for y, vals in enumerate(cols):
            assert vals == None, f"Expected grid[{x}][{y}] to be None but got {vals}"

def test_othello_size():
    """
    Testing othello board size
    """
    game = Reversi(side=8, players=2, othello=True)
    assert len(game.grid) == 8
    for cols in game.grid:
        assert len(cols) == 8, f"Expected length of row is 8, got [{len(cols)}]"

def test_othello_numplayers():
    """
    Testing othello property: num_players
    """
    game = Reversi(side=8, players=2, othello=True)
    assert game.num_players == 2, f"Only two players allowed, you have [{game.num_players}]"

def helper_apply_move(game: Reversi, moves: list[tuple[int, int]]) -> None:
    """
    A helper that adds the moves to a board and return the board
    """
    for mov in moves:
        game.apply_move(mov)

def test_othello_turn():
    """
    Testing othello property: turn, on starting position
    """
    game = Reversi(side=8, players=2, othello=True)
    assert game.turn == 1, f"Black needs to start the game"

def test_othello_piece_at():
    """
    Testing othello property: piece_at
    """
    game = Reversi(side=8, players=2, othello=True)
    assert game.piece_at((4,3)) == None

def test_othello_legal_move():
    """
    Testing othello property: legal_move
    """
    game = Reversi(side=8, players=2, othello=True)
    legal = {
        (2, 3)
        (3, 2)
        (5, 4)
        (4, 5)
    }

    for r in range(8):
        for c in range(8):
            if (r, c) in legal:
                assert game.legal_move(
                    (r, c)
                ), f"{(r,c)} is a legal move, but legal_move returned False"
            else:
                assert not game.legal_move(
                    (r, c)
                ), f"{(r,c)} is not a legal move, but legal_move returned True"

def test_othello_avalible_moves():
    """
    Testing othello property: avalible_moves
    """
    game = Reversi(side=8, players=2, othello=True)
    legal = {
        (2, 3)
        (3, 2)
        (5, 4)
        (4, 5)
    }
    assert len(game.avalible_moves) == len(legal)
    for vals in game.avalible_moves():
        assert vals in legal
    res = [*set(game.avalible_moves)]
    assert len(res) == len(legal), f"There can't be duplicates"

def test_othello_apply():
    """
    Testing a game with one applied move
    """
    game = Reversi(side=8, players=2, othello=True)
    game.apply_move((3, 2))
    assert game.turn == 2, f"it should be White's Turn"
    assert game.piece_at(3, 2) == 1, f"This should be Black"
    assert game.piece_at(3, 3) == 1, f"This piece should have been taken by Black"
    assert game.turn == 2, f"it is White's turn now"
    assert game.done == False, f"The game is not done, board needs to be full"
    assert game.outcome == [], f"There is no outcome yet, board needs to be full"

def test_othello_game_over():
    """
    Testing an endgame of othello
    """
    game = Reversi(side=8, players=2, othello=True)
    moves = [
        (3, 2),
        (2, 2),
        (1, 2),
        (1, 1),
        (0, 1),
        (0, 0),
        (5, 4),
        (5, 5),
        (5, 6),
        (6, 6),
        (7, 6),
        (7, 7),
        (2, 3),
        (0, 2),
        (1, 2),
        (1, 3),
        (1, 0),
        (2, 0),
        (3, 0),
        (4, 0),
        (5, 4),
        (0, 3),
        (5, 6),
        (1, 3),
        (7, 6),
        (4, 2),
        (4, 1),
        (2, 4),
        (1, 4),
        (1, 5),
        (0, 4),
        (0, 5),
        (0, 6),
        (0, 7)
    ]
    helper_apply_move(game, moves)
    assert game.done == True
    assert len(game.outcome) == 2
    assert 1 in game.outcome
    assert 2 in game.outcome3














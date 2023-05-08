
from reversi import Reversi, ReversiBase

def helper_avalible_legal(game: Reversi, moves: list[tuple[int, int]]):
    """
    a helper that runs a loop to check methods: legal_at, available_moves
    """
    assert len(moves) == len(game.available_moves), f"wrong number of moves"
    res = [*set(game.avalible_moves)]
    assert len(moves) == len(res), "no duplicates"
    for vals in game.available_moves:
        assert game.legal_move(vals) == True
        assert vals in moves, f"[{vals}] is not a legal move"

def helper_apply_move(game: Reversi, moves: list[tuple[int, int]]) -> None:
    """
    A helper that adds the moves to a board and return the board
    """
    for mov in moves:
        game.apply_move(mov)


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
        assert vals in legal, f"[{vals}] is not a legal move"
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
    assert game.done == True, f"There should be no avalible moves left and the players are tied"
    assert len(game.outcome) == 2, f"There are two winners, they each have 19"
    assert 1 in game.outcome
    assert 2 in game.outcome

def test_othello_6side():
    """
    Testing the initialization of a game of othello 6x6
    """
    game = Reversi(side=6, players=2, othello=True)
    assert len(game.grid) == 6
    for cols in game.grid:
        assert len(cols) == 6
    assert game.num_players == 2
    assert game.turn == 1
    pos = (2, 3)
    assert game.piece_at(pos) == 1
    zed = (0, 0)
    assert game.piece_at(zed) == None
    corr = (2, 1)
    assert game.legal_move(corr) == True
    wro = (0, 4)
    assert game.legal_move(wro) == False
    legal = {
        (2, 1)
        (1, 2)
        (3, 4)
        (4, 3)
    }
    assert len(game.available_moves) == len(legal), f"Wrong number of avalible moves"
    for r in range(6):
        for c in range(6):
            if (r, c) in legal:
                assert game.legal_move(
                    (r, c)
                ), f"{(r,c)} is a legal move, but legal_move returned False"
            else:
                assert not game.legal_move(
                    (r, c)
                ), f"{(r,c)} is not a legal move, but legal_move returned True"

def test_othello_6side():
    """
    Testing the initialization of a game of othello 6x6
    """
    game = Reversi(side=20, players=2, othello=True)
    assert len(game.grid) == 20
    for cols in game.grid:
        assert len(cols) == 20
    assert game.num_players == 2
    assert game.turn == 1
    pos = (10, 10)
    assert game.piece_at(pos) == 2
    zed = (0, 0)
    assert game.piece_at(zed) == None
    corr = (8, 9)
    assert game.legal_move(corr) == True
    wro = (0, 4)
    assert game.legal_move(wro) == False
    legal = [
        (8, 9),
        (9, 8),
        (10, 11),
        (11, 10)
    ]
    assert len(game.available_moves) == len(legal), f"Wrong number of avalible moves"
    for r in range(20):
        for c in range(20):
            if (r, c) in legal:
                assert game.legal_move(
                    (r, c)
                ), f"{(r,c)} is a legal move, but legal_move returned False"
            else:
                assert not game.legal_move(
                    (r, c)
                ), f"{(r,c)} is not a legal move, but legal_move returned True"

def test_not_othello1():
    """
    Testing the gameplay of a game of Reversu
    """
    game = Reversi(side=8, players=2, othello=False)
    legal = [
        (3, 3),
        (3, 4),
        (4, 4),
        (4, 3)
    ]
    assert len(game.avalible_moves) == len(legal)
    for vals in game.avalible_moves():
        assert game.legal_move(vals) == True
        assert vals in legal, f"[{vals}] is not a legal move"
    res = [*set(game.avalible_moves)]
    assert len(res) == len(legal), f"There can't be duplicates"
    fal = (2, 3)
    assert game.legal_move(fal) == False

def test_not_othello2():
    """
    Testing the gameplay of a game of Reversi
    """
    game = Reversi(side=9, players=3, othello=False)

    avalible = [
        (3, 3),
        (3, 4),
        (3, 5),
        (4, 3),
        (4, 4),
        (4, 5),
        (5, 3),
        (5, 4),
        (5, 5)
    ]
    helper_avalible_legal(game, avalible)
    applied = [
        (3, 3),
        (5, 5),
        (3, 5),
        (4, 4),
        (3, 4),
        (4, 5),
        (5, 4),
        (4, 3),
        (5, 3)
    ]
    helper_apply_move(game, applied)
    legal = [
        (4, 2),
        (5, 2),
        (3, 6),
        (4, 6),
        (5, 6),
        (6, 6)
    ]
    helper_avalible_legal(game, legal)

def test_not_othello3():
    """
    Testing a full game of 5x5 not othello
    """
    game = Reversi(side=5, players=3, othello=False)
    apply = [
        (1, 1),
        (1, 2),
        (1, 3),
        (2, 1),
        (2, 2),
        (2, 3),
        (3, 1),
        (3, 2),
        (3, 3),
        (1, 4),
        (2, 4),
        (0, 3),
        (3, 4),
        (0, 0),
        (2, 0),
        (1, 0),
        (0, 2),
        (0, 4),
        (0, 1),
        (3, 0),
        (4, 0),
        (4, 1),
        (4, 2),
        (4, 3),
        (4, 4)
    ]
    helper_apply_move(game, apply)
    model_ending = [
        [2, 1, 2, 3, 3],
        [2, 1, 2, 3, 1],
        [2, 1, 2, 3, 2],
        [2, 2, 2, 2, 1],
        [3, 1, 2, 3, 1]
    ]
    assert game.grid == model_ending
    assert game.done == True
    assert game.outcome == [2]













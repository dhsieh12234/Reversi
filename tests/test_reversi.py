
import pytest
from reversi import Reversi, ReversiBase

def helper_avalible_legal(game: Reversi, moves: list[tuple[int, int]]):
    """
    a helper that runs a loop to check methods: legal_at, available_moves
    """
    assert len(moves) == len(game.available_moves), f"wrong number of moves"
    res = [*set(game.available_moves)]
    assert len(moves) == len(res), "no duplicates"
    for vals in game.available_moves:
        assert game.legal_move(vals) == True
        assert vals in moves, f"[{vals}] is not a legal move"

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
    for x, cols in enumerate(game.grid):
        for y, vals in enumerate(cols):
            if x == 1:
                if y != 2 and y != 1:
                    assert vals == None
            if x == 2:
                if y != 2 and y!= 1:
                    assert vals == None
            else:
                if y != 2 and y != 1:
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
        for y, vals in enumerate(cols):
            if x == 2:
                if y != 2 and y != 3:
                    assert vals == None, f"Expected grid[{x}][{y}] to be None but got {vals}"
            if x == 3:
                if y != 3 and y != 2:
                    assert vals == None, f"Expected grid[{x}][{y}] to be None but got {vals}"
            else:
                if y != 2 and y != 3:
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

    with pytest.raises(ValueError):
        reversi = Reversi(side=20, players=10, othello=False)
        reversi.apply_move((8, 8))


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
    assert game.piece_at((0, 0)) == None

def test_othello_legal_move():
    """
    Testing othello property: legal_move
    """
    game = Reversi(side=8, players=2, othello=True)
    legal = [
        (2, 3),
        (3, 2),
        (5, 4),
        (4, 5)
    ]

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
    legal = [
        (2, 3),
        (3, 2),
        (5, 4),
        (4, 5)
    ]
    assert len(game.available_moves) == len(legal)
    for vals in game.available_moves:
        assert vals in legal, f"[{vals}] is not a legal move"
    res = [*set(game.available_moves)]
    assert len(res) == len(legal), f"There can't be duplicates"

def test_othello_apply():
    """
    Testing a game with one applied move
    """
    game = Reversi(side=8, players=2, othello=True)
    game.apply_move((3, 2))
    assert game.turn == 2, f"it should be White's Turn"
    assert game.piece_at((3, 2)) == 1, f"This should be Black"
    assert game.piece_at((3, 3)) == 1, f"This piece should have been taken by Black"
    assert game.turn == 2, f"it is White's turn now"
    assert game.done == False, f"The game is not done, board needs to be full"
    assert game.outcome == [], f"There is no outcome yet, board needs to be full"

def test_othello_game_over():
    """
    Testing an endgame of othello
    """
    game = Reversi(side=4, players=2, othello=True)
    moves = [[2, 2, 1, 1],
             [2, 2, 2, 2],
             [2, 2, 2, 2],
             [2, 2, 2, None]]
    game.load_game(1, moves)
    game.apply_move((3, 3))
    assert game.done == True, f"There should be no avalible moves left and the players are tied"
    assert len(game.outcome) == 1, f"There are two winners, they each have 19"
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
    legal = [
        (2, 1),
        (1, 2),
        (3, 4),
        (4, 3)
    ]
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

def test_othello_6_side():
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
    assert len(game.available_moves) == len(legal), "wrong number of legal moves"
    for vals in game.available_moves:
        assert game.legal_move(vals) == True
        assert vals in legal, f"[{vals}] is not a legal move"
    res = [*set(game.available_moves)]
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
    first_stage = [[None, None, None, None, None, None, None, None, None],
                   [None, None, None, None, None, None, None, None, None],
                   [None, None, None, None, None, None, None, None, None],
                   [None, None, None,    1,    2,    3, None, None, None],
                   [None, None, None,    2,    1,    3, None, None, None],
                   [None, None, None,    3,    1,    2, None, None, None],
                   [None, None, None, None, None, None, None, None, None],
                   [None, None, None, None, None, None, None, None, None],
                   [None, None, None, None, None, None, None, None, None]]
    game.load_game(1, first_stage)
    legal = [
        (2, 4),
        (2, 6),
        (3, 2),
        (3, 6),
        (4, 2),
        (4, 6),
        (5, 2),
        (5, 6),
        (6, 2),
        (6, 3),
        (6, 6)
    ]
    helper_avalible_legal(game, legal)

def test_not_othello3():
    """
    Testing a full game of 5x5 not othello
    """
    game = Reversi(side=5, players=3, othello=False)
    ending_stage = [[2, 2, 2, 2, 2],
                    [3, 2, 2, 3, 2],
                    [1, 2, 3, 3, 1],
                    [2, 2, 2, 2, 2],
                    [2, 2, None, None, None]]
    game.load_game(1, ending_stage)
    game.apply_move((4, 2))
    game.apply_move((4, 3))
    game.apply_move((4, 4))
    model_ending = [[2, 2, 2, 2, 2],
                    [3, 2, 2, 2, 2],
                    [1, 2, 3, 2, 1],
                    [2, 1, 2, 3, 2],
                    [2, 2, 2, 2, 3]]
    assert game.grid == model_ending
    assert game.done == True
    assert game.outcome == [2]

def test_load_game():
    """
    Test the load game feature
    """
    game = Reversi(side=8, players=2, othello=True)
    move = (3, 5)
    game.apply_move(move)
    curr = game.grid
    game.load_game(2, curr)
    assert game.grid == curr, "Game loads wrong, pieces disrupted"

def test_load_game_errors1():
    """
    Testing the player number error function of the load_game method
    """

    with pytest.raises(ValueError):
        game = Reversi(side=8, players=2, othello=True)
        game.apply_move((3, 5))
        curr = game.grid
        game.load_game(4, curr)

def test_load_game_errors2():
    """
    Testing the size error fuction of the load_game method
    """

    with pytest.raises(ValueError):
        game = Reversi(side=8, players=2, othello=True)
        curr = []
        game.load_game(1, curr)

def test_load_game_errors3():
    """
    Testing the players attribute error
    """
    with pytest.raises(ValueError):
        game = Reversi(side=8, players=2, othello=True)
        curr = game.grid
        curr[0][1] = 3
        game.load_game(1, curr)

def test_skip_move():
    """
    Test that tests the skip move function
    Black should have to skip their move
    """
    game = Reversi(side=8, players=2, othello=True)
    skip_board = [[   1,    1,    1,    1,    1, None, None, None],
                  [   2,    2,    1, None,    1, None, None, None],
                  [   1,    1,    1,    1,    1, None, None, None],
                  [None, None,    1,    1,    1, None, None, None],
                  [None, None,    1,    1,    1, None, None, None],
                  [None, None, None, None, None, None, None, None],
                  [None, None, None, None, None, None, None, None],
                  [None, None, None, None, None, None, None, None]]
    game.load_game(2, skip_board)
    game.apply_move((1, 3))
    assert game.turn == 2, "Turn skipping doesn't work"

def test_simulate_move_1():
    """
    Test simulating a move that doesn't end the game
    """

    game = Reversi(side=8, players=2, othello=True)

    grid_orig = game.grid

    future_reversi = game.simulate_moves([(3, 2)])

    legal = [
        (3, 2),
        (2, 3),
        (4, 5),
        (5, 4)
    ]

    # Check that the original game state has been preserved
    assert game.grid == grid_orig, "simulate move doesn't work"
    assert game.turn == 1, "turn not updating"
    assert set(game.available_moves) == set(legal), "move options arn't working"
    assert not game.done
    assert game.outcome == []

    # Check that the returned object corresponds to the
    # state after making the move.
    legal = {
        (2, 2),
        (2, 4),
        (4, 2)
    }
    assert future_reversi.grid != grid_orig
    assert future_reversi.turn == 2
    assert set(future_reversi.available_moves) == set(legal)
    assert not future_reversi.done
    assert future_reversi.outcome == []


def test_simulate_move_2():
    """
    Test simulating a move that results in Player 1 winning
    """

    game = Reversi(side=8, players=2, othello=True)

    win_game = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1],
                [2, 1, 1, 2, 1, 2, 1, 1],
                [1, 2, 1, 2, 1, 1, 1, 1],
                [2, 1, 1, 1, 2, 2, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1],
                [2, 1, 1, 1, 1, 1, 1, 2],
                [2, 2, 2, 2, 2, 2, 2, None]]
    game.load_game(1, win_game)
    grid_ori = game.grid
    legal = [(7, 7)]
    future_reversi = game.simulate_moves([(7, 7)])
    # Check that the original game state has been preserved
    assert game.grid == grid_ori
    assert game.turn == 1
    assert set(game.available_moves) == set(legal)
    assert not game.done
    assert game.outcome == []

    # Check that the returned values correspond to the
    # state after making the move.
    assert future_reversi.grid != grid_ori
    assert future_reversi.done
    assert future_reversi.outcome == [1]


def test_simulate_move_3():
    """
    Test simulating a move that results in a tie
    """

    game = Reversi(side=8, players=2, othello=True)

    tie_game = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1],
                [2, 2, 2, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 2, 1, None]]
    game.load_game(2, tie_game)
    grid_orig = game.grid
    future_reversi = game.simulate_moves([(7, 7)])
    legal = {
        (7, 7)
    }

    # Check that the original game state has been preserved
    assert game.grid == grid_orig
    assert game.turn == 2
    assert set(game.available_moves) == set(legal)
    assert not game.done
    assert game.outcome == []

    # Check that the returned values correspond to the
    # state after making the move.
    assert future_reversi.grid != grid_orig
    assert future_reversi.done
    assert sorted(future_reversi.outcome) == [1, 2]


def test_simulate_moves_4():
    """
    Test that calling simulate_moves with an invalid position
    raises a ValueError exception.
    """
    with pytest.raises(ValueError):
        reversi = Reversi(side=7, players=2, othello=True)
        future_reversi = reversi.simulate_moves([(-1, -1)])

    with pytest.raises(ValueError):
        reversi = Reversi(side=7, players=2, othello=True)
        future_reversi = reversi.simulate_moves([(8, 8)])

def test_simulate_moves_5():
    """
    Test that calls multiple simulated moves
    """
    game = Reversi(side=8, players=2, othello=True)

    grid_orig = game.grid

    future_reversi = game.simulate_moves([(2, 3)])
    legal = [
        (3, 2),
        (2, 3),
        (4, 5),
        (5, 4)
    ]

    # Check that the original game state has been preserved
    assert game.grid == grid_orig
    assert game.turn == 1
    assert set(game.available_moves) == set(legal)
    assert not game.done
    assert game.outcome == []

    # Check that the returned object corresponds to the
    # state after making the move.
    legal = [
        (2, 4),
        (4, 2),
        (2, 2)
    ]
    assert future_reversi.grid != grid_orig
    assert future_reversi.turn == 2
    assert set(future_reversi.available_moves) == set(legal)
    assert not future_reversi.done
    assert future_reversi.outcome == []

    final_reversi = future_reversi.simulate_moves([(2, 2)])
    legal = [
        (2, 1),
        (3, 2),
        (5, 4),
        (4, 5)
    ]

    assert final_reversi.grid != future_reversi.grid
    assert final_reversi.turn == 1
    assert set(final_reversi.available_moves) == set(legal)
    assert not final_reversi.done
    assert final_reversi.outcome == []


def test_endgame_8():
    """
    a test ending for the 8 by 8 game with 2 players, one winner
    """
    game = Reversi(side=8, players=2, othello=False)
    final_board = [[1, 2, 1, 1, 1, 1, 1, 1],
                   [2, 1, 1, 1, 2, 1, 1, 1],
                   [2, 2, 2, 2, 1, 1, 2, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1],
                   [2, 2, 2, 2, 2, 2, 2, 2],
                   [1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1]]
    game.load_game(1, final_board)
    assert game.done == True, "the are no moves to make, game should be dome"
    assert len(game.outcome) == 1
    assert 1 in game.outcome

def test_endgame_8_tie():
    """
    A test ending of a 8 by 8 two player game with a tied ending and full board
    """
    game = Reversi(side=8, players=2, othello=False)
    final_board = [[1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1],
                   [2, 2, 2, 2, 2, 2, 2, 2],
                   [1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1],
                   [2, 2, 2, 2, 2, 2, 2, 2],
                   [2, 2, 2, 2, 2, 2, 2, 2],
                   [2, 2, 2, 2, 2, 2, 2, 2]]
    game.load_game(2, final_board)
    assert game.done == True, "the are no moves to make, game should be dome"
    assert len(game.outcome) == 2
    assert 1 in game.outcome
    assert 2 in game.outcome

def test_endgame_7_winner():
    """
    A test ending of a 7 by 7 game with three players, one winning
    """
    game = Reversi(side=7, players=3, othello=False)
    final_board = [[1, 2, 3, 1, 1, 2, 3],
                   [3, 3, 3, 3, 3, 3, 3],
                   [2, 3, 3, 3, 1, 3, 3],
                   [2, 2, 1, 1, 3, 3, 3],
                   [3, 3, 3, 3, 3, 3, 3],
                   [3, 3, 3, 3, 3, 3, 3],
                   [3, 3, 3, 3, 3, 3, 3]]
    game.load_game(3, final_board)
    assert game.done == True, "the are no moves to make, game should be dome"
    assert len(game.outcome) == 1
    assert 3 in game.outcome

def test_endgame_7_tie():
    """
    A test ending of a 7 by 7 game with three players, two tieing
    """
    game = Reversi(side=7, players=3, othello=False)
    final_board = [[1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1],
                   [2, 2, 2, 2, 2, 2, 2],
                   [2, 2, 2, 2, 2, 2, 2],
                   [2, 2, 2, 2, 2, 2, 2],
                   [3, 3, 3, 3, 3, 3, 3]]
    game.load_game(1, final_board)
    assert game.done == True, "No more avalible squares, game is over"
    assert len(game.outcome) == 2
    assert 1 in game.outcome
    assert 2 in game.outcome

def test_early_ending_8():
    """
    Both players have no moves before game is over, but one wins
    """
    game = Reversi(side=8, players=2, othello=False)
    final_board = [[   1,    1,    1, None, None, None, None, None],
                   [None,    1,    1, None, None, None, None, None],
                   [None,    1,    1,    1,    1, None, None, None],
                   [None, None, None,    1,    1, None, None, None],
                   [None, None, None,    1,    1, None, None, None],
                   [None, None, None,    1,    1, None, None, None],
                   [None, None, None, None, None, None, None, None],
                   [None, None, None, None, None, None, None, None]]
    game.load_game(2, final_board)
    assert game.done == True, "the are no moves to make, game should be dome"
    assert len(game.outcome) == 1, "1 has more pieces and should be winning"
    assert 1 in game.outcome, "1 has more pieces and should be winning"







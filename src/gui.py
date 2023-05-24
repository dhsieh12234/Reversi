import os
import sys
import math
import click
from typing import List, Tuple, Optional
from reversi import Reversi, Board, BoardGridType, COLORS
from bot import ReversiBot
from termcolor import colored, cprint

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame  # pylint: disable=wrong-import-position


@click.command("gui")
@click.option("-n", "--num-players", default = 2)
@click.option("-s", "--board-size", default = 8)
@click.option("--othello", is_flag = True)
@click.option("--non-othello", is_flag = True)
@click.option("--bot",
              type = click.Choice(["random", "smart", "very-smart"]),
              default = None)
def run_game(num_players: int, board_size: int, othello: bool, 
             non_othello: bool, bot: Optional[str]):
    Game_Interface(Reversi(board_size, num_players, not non_othello))

class Game_Interface:
    """
    Class for a GUI-based reversi game
    """

    window : int
    border : int
    grid : List[List[bool]]
    surface : pygame.surface.Surface
    clock : pygame.time.Clock

    def __init__(self, game: Reversi):
        """
        Constructor

        Parameters:
            window : int : height of window
            border : int : number of pixels to use as border around elements
            cells_side : int : number of cells on a side of a square bitmap grid
        """
        self.game = game
        self.window = 600
        self.border = 10
        self.cells_side = self.game.size
        self.square = (self.window - 2 * self.border) // self.cells_side
        self.players = game.num_players
        player_1_color = (155, 155, 155)
        player_2_color = (105, 105, 105)
        player_3_color = (172, 55, 238)
        player_4_color = (8, 255, 8)
        player_5_color = (255, 173, 0)
        player_6_color = (251, 72, 196)
        player_7_color = (235, 33, 46)
        player_8_color = (199, 36, 177)
        player_9_color = (254, 219, 0)
        self.color_list = [player_1_color, player_2_color, player_3_color, 
                            player_4_color, player_5_color, player_6_color,
                            player_7_color, player_8_color, player_9_color]
        # Initialize Pygame
        pygame.init()
        # Set window title
        pygame.display.set_caption("BitEdit")
        # Set window size
        self.surface = pygame.display.set_mode((self.window + self.border + self.square * 1.5,
                                                self.window))
        self.clock = pygame.time.Clock()

        self.event_loop()



    def piece_placer(self, loc) -> None:
        """
        Understand which point in grid is being selected by click.

        Paramaters: self and the location of a mouse button up.

        Returns: nothing
        """
        x, y = loc
        self_x = None
        self_y = None
        grid_edge = self.border + self.square * self.cells_side
        if self.border < x < grid_edge:
            self_x = (x - self.border) // (self.square)
        if self.border < x < grid_edge:
            self_y = (y - self.border) // (self.square)
        if self_x is not None and self_y is not None and self.game.legal_move((self_y, self_x)):
            self.game.grid[self_y][self_x] = self.game.turn
            self.game.apply_move((self_y, self_x))
        
    def game_over(self) -> None:
        list_str = map(str, self.game.outcome)
        winners = ' '.join(list_str)
        if len(self.game.outcome) > 1:
            self.surface.fill((255, 87, 51))
            my_font = pygame.font.SysFont('Impact', 155)
            text_surface = my_font.render('GAME OVER', False, (35, 35, 35))
            self.surface.blit(text_surface, (0, 0))
            tie_txt = "TIE BETWEEN {}"
            tie_txt = tie_txt.format(winners)
            text_surface = my_font.render(tie_txt, False, (35, 35, 35))
            self.surface.blit(text_surface, (0, 300))

        r_tot = 0
        g_tot = 0
        b_tot = 0
        for x, y in enumerate(self.game.outcome):
            r, g, b = self.color_list[x]
            r_tot += r
            g_tot += g
            b_tot += b
        r_tot = r_tot / len(self.game.outcome)
        g_tot = g_tot / len(self.game.outcome)
        b_tot = b_tot / len(self.game.outcome)
        win_color = (r_tot, g_tot, b_tot)

        self.surface.fill(win_color)
        my_font = pygame.font.SysFont('Impact', 155)
        text_surface = my_font.render('GAME OVER', False, (35, 35, 35))
        self.surface.blit(text_surface, (0, 0))
        my_font = pygame.font.SysFont('Impact', 117)
        winner = "PLAYER {} WINS"
        winner = winner.format(winners)
        text_surface = my_font.render(winner, False, (35, 35, 35))
        self.surface.blit(text_surface, (0, 300))




    def draw_window(self) -> None:
        """
        Draws the contents of the window

        Parameters: none beyond self

        Returns: nothing
        """
        turn_color = self.color_list[self.game.turn] - 1
        background_color = (35, 35, 35)
        board_color = (75, 75, 75)
        circle_radius = self.square // 2 - 5

        #Create the Background and Turn
        turn_center = (self.border + self.square * (self.cells_side + 1), 
                        self.border + 2.5 * self.square)
        turn_rect = (self.border + self.square * (self.cells_side + 0.5), 
                    self.border + 2 * self.square , self.square, self.square)
        text_loc = (self.border + self.square * (self.cells_side + 0.5), 
                    self.border + 1.5 * self.square)
        font_size = int(self.square // 2.2)

        self.surface.fill(background_color)
        my_font = pygame.font.SysFont('Impact', font_size)
        text_surface = my_font.render('TURN', False, board_color)
        self.surface.blit(text_surface, text_loc)
        pygame.draw.rect(self.surface, board_color, turn_rect)
        pygame.draw.circle(self.surface, turn_color, turn_center, circle_radius)

        
        #Places Pieces
        for row in range(self.cells_side):
            for col in range(self.cells_side):
                rect = (self.border + col * self.square,
                        self.border + row * self.square,
                        self.square, self.square)
                circle_center = (self.border + (col + 0.5) * self.square, self.border + (row + 0.5) * self.square)
                pygame.draw.rect(self.surface, board_color,
                                 rect=rect)
                if self.game.legal_move((row, col)):
                    pygame.draw.rect(self.surface, turn_color, rect=rect)
                pygame.draw.rect(self.surface, background_color,
                                     rect=rect, width=1)
                if self.game.grid[row][col] is not None:
                    pygame.draw.circle(self.surface, self.color_list[self.game.grid[row][col] - 1], circle_center, circle_radius)

        if self.game.done:
            self.game_over()

    def event_loop(self) -> None:
        """
        Handles user interactions

        Parameters: none beyond self

        Returns: nothing
        """
        while True:
            # Process Pygame events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.game.done:
                    self.game_over()
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos2 = pygame.mouse.get_pos()
                    loc2 = [pos2[0], pos2[1]]
                    self.piece_placer(loc2)


                # Handle any other event types here

            # Update the display
            self.draw_window()
            pygame.display.update()
            self.clock.tick(24)


if __name__ == "__main__":
    run_game()

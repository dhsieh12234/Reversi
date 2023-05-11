import os
import sys
import math
from typing import List, Tuple
from mocks import ReversiMock, BoardGridType

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame  # pylint: disable=wrong-import-position

side: int = int(sys.argv[1])

class Game_Interface:
    """
    Class for a GUI-based reversi game
    """

    window : int
    border : int
    grid : List[List[bool]]
    surface : pygame.surface.Surface
    clock : pygame.time.Clock

    def __init__(self, game: ReversiMock):
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
        self.grid = self.game.grid
        self.square = (self.window - 2 * self.border) // self.cells_side
        self.players = game.num_players
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
            self.grid[self_y][self_x] = self.game.turn
            self.game.apply_move((self_y, self_x))
        
    def game_over(self) -> None:
        player_1_color = (155, 155, 155)
        player_2_color = (105, 105, 105)
        if self.game.outcome[0] == 1:
            win_color = player_1_color
        if self.game.outcome[0] == 2:
            win_color = player_2_color
        self.surface.fill(win_color)
        my_font = pygame.font.SysFont('Impact', 155)
        text_surface = my_font.render('GAME OVER', False, (35, 35, 35))
        self.surface.blit(text_surface, (0, 0))
        my_font = pygame.font.SysFont('Impact', 117)
        winner = "PLAYER {} WINS"
        winner = winner.format(self.game.outcome[0])
        text_surface = my_font.render(winner, False, (35, 35, 35))
        self.surface.blit(text_surface, (0, 300))




    def draw_window(self) -> None:
        """
        Draws the contents of the window

        Parameters: none beyond self

        Returns: nothing
        """
        player_1_color = (155, 155, 155)
        player_2_color = (105, 105, 105)
        turn_color = (0, 0, 0)
        if self.game.turn == 1:
            turn_color = player_1_color
        if self.game.turn == 2:
            turn_color = player_2_color
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
                if self.grid[row][col] == 1:
                    pygame.draw.circle(self.surface, player_1_color, circle_center, circle_radius)
                elif self.grid[row][col] == 2:
                    pygame.draw.circle(self.surface, player_2_color, circle_center, circle_radius)
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
    Game_Interface(ReversiMock(side, 2, True))

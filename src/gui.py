import os
import sys
import math
from typing import List, Tuple
from mocks import ReversiStub, BoardGridType

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

    def __init__(self, game: ReversiStub = ReversiStub(side, 2, False)):
        """
        Constructor

        Parameters:
            window : int : height of window
            border : int : number of pixels to use as border around elements
            cells_side : int : number of cells on a side of a square bitmap grid
        """
        self.window = 600
        self.border = 10
        self.cells_side = side
        self.grid = [[None] * self.cells_side for i in range(self.cells_side)]
        self.tool = "Black"
        self.square = (self.window - 2 * self.border) // self.cells_side
        self.players = game.num_players
        # Initialize Pygame
        pygame.init()
        # Set window title
        pygame.display.set_caption("BitEdit")
        # Set window size
        self.surface = pygame.display.set_mode((self.window + self.border + self.cells_side,
                                                self.window))
        self.clock = pygame.time.Clock()

        self.grid[0][0] = 1
        self.grid[self.cells_side - 1][self.cells_side - 1] = 1
        self.grid[self.cells_side - 1][0] = 2
        self.grid[0][self.cells_side - 1] = 2

        self.event_loop()



    def grid_selector(self, loc) -> None:
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
        if self.tool == "Black" and self_x is not None and self_y is not None:
            self.grid[self_y][self_x] = True
        elif self.tool == "White" and self_x is not None and self_y is not None:
            self.grid[self_y][self_x] = False
        elif self.tool == "Fill" and self_x is not None and self_y is not None:
            self.fill_it_up(self_y, self_x, self.grid[self_y][self_x])



    def draw_window(self) -> None:
        """
        Draws the contents of the window

        Parameters: none beyond self

        Returns: nothing
        """
        cells_side = len(self.grid)

        # Background
        self.surface.fill((17, 0, 141))

        for row in range(cells_side):
            for col in range(cells_side):
                rect = (self.border + col * self.square,
                        self.border + row * self.square,
                        self.square, self.square)
                circle_center = (self.border + (col + 0.5) * self.square, self.border + (row + 0.5) * self.square)
                fill = (127, 127, 127)
                border = True
                pygame.draw.rect(self.surface, color=fill,
                                 rect=rect)
                pygame.draw.rect(self.surface, color=(0, 0, 0),
                                     rect=rect, width=1)
                if self.grid[row][col] == 1:
                    fill = (188, 188, 188)
                    border = True
                    pygame.draw.circle(self.surface, (188, 188, 188), circle_center, self.square // 2 - 5)
                elif self.grid[row][col] == 2:
                    fill = (66, 66, 66)
                    border = True
                    pygame.draw.circle(self.surface, (66, 66, 66), circle_center, self.square // 2 - 5)

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
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos2 = pygame.mouse.get_pos()
                    loc2 = [pos2[0], pos2[1]]
                    self.grid_selector(loc2)


                # Handle any other event types here

            # Update the display
            self.draw_window()
            pygame.display.update()
            self.clock.tick(24)


if __name__ == "__main__":
    Game_Interface(ReversiStub(side, 2, False))

import os
import sys
import math
from typing import List, Tuple

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame  # pylint: disable=wrong-import-position


class BitEdit:
    """
    Class for a GUI-based bitmap editor
    """

    window : int
    border : int
    grid : List[List[bool]]
    surface : pygame.surface.Surface
    clock : pygame.time.Clock

    def __init__(self, window: int = 600, border: int = 10,
                 cells_side: int = 32):
        """
        Constructor

        Parameters:
            window : int : height of window
            border : int : number of pixels to use as border around elements
            cells_side : int : number of cells on a side of a square bitmap grid
        """
        self.window = window
        self.border = border
        self.grid = [[False] * cells_side for i in range(cells_side)]
        self.tool = "Black"
        self.cells_side = cells_side

        self.square = (self.window - 2 * self.border) // cells_side
        self.mini_left = 2 * self.border + self.square * cells_side
        self.mini_top = (self.window - cells_side) // 2
        self.black_tool_center = (self.mini_left + cells_side // 2,
                             self.border + cells_side // 2)
        self.white_tool_center = (self.mini_left + cells_side // 2,
                             self.border + 3 * (cells_side // 2))
        self.fill_tool_center = (self.mini_left + cells_side // 2,
                             2 * self.border + 5 * (cells_side // 2))

        # Initialize Pygame
        pygame.init()
        # Set window title
        pygame.display.set_caption("BitEdit")
        # Set window size
        self.surface = pygame.display.set_mode((window + border + cells_side,
                                                window))
        self.clock = pygame.time.Clock()

        self.event_loop()


    def tool_selector(self, loc) -> None:
        """
        Understand which tool is being selected by click.

        Parameters: self and the location of a mouse button down.

        Returns: nothing
        """
        x, y = loc
        if math.sqrt((x - self.black_tool_center[0]) ** 2 + \
        (y - self.black_tool_center[1]) ** 2) < self.cells_side // 2:
            self.tool = "Black"
        elif math.sqrt((x - self.white_tool_center[0]) ** 2 + \
        (y - self.white_tool_center[1]) ** 2) < self.cells_side // 2:
            self.tool = "White"
        elif math.sqrt((x - self.fill_tool_center[0]) ** 2 + \
        (y - self.fill_tool_center[1]) ** 2) < self.cells_side // 2:
            self.tool = "Fill"

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

    def fill_it_up(self, x, y, current_color) -> None:
        """
        "Flood fill" (the paint-bucket tool) a grid of booleans
        Change a cell in the grid to black (True) and its neighboring cell, and
        their neighbors, stopping when encountering an already-black (True)
        cell in a given direction
        Directions are N, E, S, and W, but not diagonal

        Parameters:
        self
        x: x value of the square being filled.
        y: y value of the sqare being filled.
        current color: boolean of the color that is being changed from.

        Returns: nothing
        """
        if x > self.cells_side - 1 or y > self.cells_side - 1 or x < 0 or \
        y < 0 or self.grid[x][y]!= current_color:
            return
        else:

            self.grid[x][y] = not current_color
            self.fill_it_up(x + 1, y, current_color)
            self.fill_it_up(x - 1, y, current_color)
            self.fill_it_up(x, y + 1, current_color)
            self.fill_it_up(x, y - 1, current_color)




    def draw_window(self) -> None:
        """
        Draws the contents of the window

        Parameters: none beyond self

        Returns: nothing
        """
        cells_side = len(self.grid)

        # Background
        self.surface.fill((128, 128, 128))

        rect = (self.mini_left, self.mini_top, cells_side, cells_side)
        pygame.draw.rect(self.surface, color=(255, 255, 255),
                         rect=rect)


        pygame.draw.circle(self.surface, color=(0, 0, 0),
                        center=self.black_tool_center, radius=cells_side // 2)
        pygame.draw.circle(self.surface, color=(255, 255, 255),
                        center=self.white_tool_center, radius=cells_side // 2)
        pygame.draw.circle(self.surface, color=(0, 0, 0),
                        center=self.white_tool_center, radius=cells_side // 2,
                           width=2)
        pygame.draw.circle(self.surface, color=(0, 0, 0),
                           center=self.fill_tool_center, radius=cells_side // 2)
        pygame.draw.circle(self.surface, color=(255, 255, 255),
                           center=self.fill_tool_center, radius=cells_side // 4,
                           width=2)

        if self.tool == "Black":
            pygame.draw.circle(self.surface, color=(64, 224, 208),
            center=self.black_tool_center, radius=cells_side // 2, width = 2)
        if self.tool == "White":
            pygame.draw.circle(self.surface, color=(64, 224, 208),
            center=self.white_tool_center, radius=cells_side // 2, width = 2)
        if self.tool == "Fill":
            pygame.draw.circle(self.surface, color=(64, 224, 208),
                center=self.fill_tool_center, radius=cells_side // 2, width = 2)


        for row in range(cells_side):
            for col in range(cells_side):
                rect = (self.border + col * self.square,
                        self.border + row * self.square,
                        self.square, self.square)
                if self.grid[row][col]:
                    fill = (0, 0, 0)
                    border = False
                    mrect = (self.mini_left + col, self.mini_top + row, 1, 1)
                    pygame.draw.rect(self.surface, color=(0, 0, 0),
                                     rect=mrect)
                else:
                    fill = (255, 255, 255)
                    border = True
                pygame.draw.rect(self.surface, color=fill,
                                 rect=rect)
                if border:
                    pygame.draw.rect(self.surface, color=(0, 0, 0),
                                     rect=rect, width=1)

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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    loc = [pos[0], pos[1]]
                    self.tool_selector(loc)
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
    BitEdit()

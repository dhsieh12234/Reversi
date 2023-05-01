"""
Bots for Reversi
(and command for running simulations with bots)
"""

import random
from typing import Union

import click

from reversi import ReversiBase

#
# BOTS
#

class RandomBot:
    """
    2 Random Bots playing each other. Records the number of wins by 
    Bot 1 and the number of wins by Bot 2.
    """

    
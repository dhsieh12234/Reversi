from typing import List, Tuple, Optional
import sys
from mocks import ReversiStub

side: int = int(sys.argv[1])
game: ReversiStub = ReversiStub(side, 2, False)
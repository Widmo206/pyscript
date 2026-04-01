"""LevelState class for keeping track of the tile action history

Created on 2026.03.26
Contributors:
    Romcode
"""

from dataclasses import dataclass

from matrix import Matrix
from tile_model import TileModel


@dataclass(frozen=True)
class LevelState:
    tile_models: Matrix[TileModel]

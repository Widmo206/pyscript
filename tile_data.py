"""TileData class for managing tile data

Created on 2026.02.25
Contributors:
    Romcode
"""

from dataclasses import dataclass

from enums import Direction, TileType


@dataclass
class TileData:
    tile_type: TileType = TileType.EMPTY
    tile_direction: Direction = Direction.RIGHT

    def __post_init__(self) -> None:
        self.tile_type = TileType.normalize(self.tile_type)
        self.tile_direction = Direction.normalize(self.tile_direction)

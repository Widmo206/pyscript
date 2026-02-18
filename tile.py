"""Tile class for tile behavior and remote TileLabel control

Created on 2026.01.28
Contributors:
    Romcode
"""

from dataclasses import dataclass

from enums import Direction, TileActionType, TileType
from events import TileTypeChanged
from tile_action import TileAction


class Tile:
    def __init__(self, tile_type: TileType | str = TileType.EMPTY) -> None:
        @dataclass(frozen=True, slots=True)
        class InstanceTileTypeChanged(TileTypeChanged):
            pass

        self.tile_type_changed = InstanceTileTypeChanged
        self.tile_type = TileType.normalize(tile_type)

    def get_action(self) -> TileAction | None:
        if self.tile_type == TileType.PLAYER:
            # TODO: Implement action choice
            return TileAction(TileActionType.MOVE, Direction.UP)
        else:
            return None

    def set_tile_type(self, tile_type: TileType | str) -> None:
        self.tile_type = TileType.normalize(tile_type)
        self.tile_type_changed(self.tile_type)

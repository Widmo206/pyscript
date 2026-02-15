"""TileAction class used by tiles during a tilemap cycle

Created on 2026.02.15
Contributors:
    Romcode
"""

from typing import NamedTuple

from enums import Direction, TileActionType


class TileAction(NamedTuple):
    type: TileActionType
    direction: Direction | None = None

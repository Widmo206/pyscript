"""TileModel class that holds tile data and can hold a processor

Created on 2026.03.01
Contributors:
    Romcode
"""

from dataclasses import dataclass, field

import logging

from enums import TileAction, TileType
from matrix import Matrix
from parser import Processor
from tile_data import TileData

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class TileModel:
    tile_data: TileData = field(default_factory=TileData)
    processor: Processor | None = None

    def __post_init__(self) -> None:
        if self.processor is None and self.tile_data.tile_type == TileType.PLAYER:
            object.__setattr__(self, "processor", Processor([]))

    def get_action(
        self,
        x: int,
        y: int,
        tile_data_matrix: Matrix[TileData]
    ) -> TileAction | None:
        if self.processor is not None:
            return self.processor.advance(x, y, tile_data_matrix)

        match self.tile_data.tile_type:
            case TileType.PLAYER:
                logger.error("Player tile model at (%d, %d) has no processor")
                return None

            case TileType.ENEMY:
                # TODO: Implement enemy AI.
                return None

            case _:
                return None

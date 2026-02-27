"""LevelModel class to handle level logic and interact with LevelController and LevelView

Created on 2026.02.18
Contributors:
    Romcode
"""

from __future__ import annotations
from dataclasses import dataclass
import logging
from pathlib import Path

from enums import Direction, TileAction, TileType
import events
from level import Level
from matrix import Matrix
from tile_data import TileData

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class LevelModel:
    level: Level
    tile_data_matrix: Matrix[TileData]

    @classmethod
    def from_path(cls, path: Path) -> LevelModel:
        level = Level.from_path(path)
        tile_data = level.get_tile_data_matrix()

        return cls(level, tile_data)

    def __post_init__(self) -> None:
        events.ProcessorAdvanced.connect(self._on_processor_advanced)
        events.LevelOpened(self.level)

    def cycle(self, player_tile_action: TileAction | None = None) -> None:
        action_matrix = Matrix(
            self.tile_data_matrix.width,
            self.tile_data_matrix.height,
            (
                (
                    player_tile_action
                    if tile_data.tile_type == TileType.PLAYER
                    else self.get_tile_action(x, y)
                )
                for x, y, tile_data
                in self.tile_data_matrix.iter_xy()
            ),
        )

        for x, y, action in action_matrix.iter_xy():
            self.process_tile_action(x, y, action)

    def destroy(self) -> None:
        events.ProcessorAdvanced.disconnect(self._on_processor_advanced)
        events.LevelClosed()

    def get_tile_action(self, x: int, y: int) -> TileAction | None:
        try:
            tile_data = self.tile_data_matrix.get(x, y)
        except IndexError:
            logger.error(f"No tile data at ({x}, {y})")
            return None

        match tile_data.tile_type:
            case TileType.PLAYER:
                logger.error("Cannot get player tile action, ask pyscript processor instead")
                return None

            case TileType.ENEMY:
                # TODO: Implement enemy AI.
                return None

            case _:
                return None

    def move_tile(self, x: int, y: int, direction: Direction) -> None:
        to_x = x + direction.x
        to_y = y + direction.y

        try:
            from_tile_data = self.tile_data_matrix.get(x, y)
            to_tile_data = self.tile_data_matrix.get(to_x, to_y)
            assert to_tile_data.tile_type.is_walkable
        except (IndexError, AssertionError):
            return

        logger.debug(
            "Moving tile %s from (%i, %i) in direction %s (%s)",
            from_tile_data.tile_type,
            x,
            y,
            direction,
            to_tile_data.tile_type,
        )
        self.tile_config(to_x, to_y, from_tile_data.tile_type, from_tile_data.tile_direction)
        self.tile_config(x, y, TileType.EMPTY, Direction.RIGHT)

    def process_tile_action(self, x: int, y: int, action: TileAction | None) -> None:
        tile_data = self.tile_data_matrix.get(x, y)

        match action:
            case TileAction.MOVE_FORWARD:
                self.move_tile(x, y, tile_data.tile_direction)

            case TileAction.MOVE_BACK:
                self.move_tile(x, y, -tile_data.tile_direction)

            case TileAction.TURN_LEFT:
                self.tile_config(x, y, tile_direction=tile_data.tile_direction.rotate(False))

            case TileAction.TURN_RIGHT:
                self.tile_config(x, y, tile_direction=tile_data.tile_direction.rotate())

            case TileAction.ATTACK:
                # TODO: Implement attacking.
                pass

            case _:
                pass

    def tile_config(
        self,
        x: int,
        y: int,
        tile_type: TileType | str | None = None,
        tile_direction: Direction | None = None,
    ) -> None:
        try:
            tile_data = self.tile_data_matrix.get(x, y)
        except IndexError:
            logger.error(f"No tile model at ({x}, {y})")
            return

        if tile_type is not None:
            tile_data.tile_type = TileType.normalize(tile_type)
        if tile_direction is not None:
            tile_data.tile_direction = Direction.normalize(tile_direction)

        events.TileDataChanged(x, y, tile_type, tile_direction)

    def _on_processor_advanced(self, event: events.ProcessorAdvanced) -> None:
        self.cycle(event.player_tile_action)

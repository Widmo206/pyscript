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
from tile_model import TileModel

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class LevelModel:
    level: Level
    tile_models: tuple[TileModel]

    @classmethod
    def from_path(cls, path: Path) -> LevelModel:
        level = Level.from_path(path)
        tile_models = tuple(
            TileModel(tile_type, tile_direction)
            for tile_type, tile_direction
            in level.iter_tile_data()
        )

        return cls(level, tile_models)

    def __post_init__(self) -> None:
        events.PlayerTileActionRequested.connect(self._on_player_tile_action_requested)
        events.LevelOpened(self.level)

    def cycle(self, player_tile_action: TileAction | None = None) -> None:
        # TODO: Remove manual movement
        actions = [
            (
                player_tile_action
                if self.get_tile_model(x, y).tile_type == TileType.PLAYER
                else self.get_tile_action(x, y)
            )
            for y in range(self.level.height)
            for x in range(self.level.width)
        ]

        for y in range(self.level.height):
            for x in range(self.level.width):
                action = actions[y * self.level.width + x]
                tile_model = self.get_tile_model(x, y)

                match action:
                    case TileAction.MOVE_FORWARD:
                        self.move_tile(x, y, tile_model.tile_direction)

                    case TileAction.MOVE_BACK:
                        self.move_tile(x, y, -tile_model.tile_direction)

                    case TileAction.TURN_LEFT:
                        self.tile_config(x, y, tile_direction=tile_model.tile_direction.rotate(False))

                    case TileAction.TURN_RIGHT:
                        self.tile_config(x, y, tile_direction=tile_model.tile_direction.rotate())

                    case TileAction.ATTACK:
                        pass

                    case _:
                        pass

    def destroy(self) -> None:
        events.PlayerTileActionRequested.disconnect(self._on_player_tile_action_requested)
        events.LevelClosed()

    def get_tile_action(self, x: int, y: int) -> TileAction | None:
        tile_model = self.get_tile_model(x, y)

        if tile_model is None:
            logger.error(f"No tile model at ({x}, {y})")
            return None

        if tile_model.tile_type == TileType.PLAYER:
            # TODO: Implement action choice
            return TileAction.MOVE_FORWARD
        else:
            return None

    def get_tile_model(self, x: int, y: int) -> TileModel | None:
        try:
            assert 0 <= x < self.level.width
            assert 0 <= y < self.level.height
            return self.tile_models[y * self.level.width + x]
        except (AssertionError, IndexError):
            return None

    def move_tile(self, x: int, y: int, direction: Direction) -> None:
        to_x = x + direction.x
        to_y = y + direction.y
        from_tile_model = self.get_tile_model(x, y)
        to_tile_model = self.get_tile_model(to_x, to_y)

        if (
            from_tile_model is None
            or to_tile_model is None
            or not to_tile_model.tile_type.is_walkable
        ):
            return

        logger.debug(
            "Moving tile '%s' from (%i, %i) in direction '%s' ('%s')",
            from_tile_model.tile_type.name,
            x,
            y,
            direction.name,
            to_tile_model.tile_type.name,
        )
        self.tile_config(to_x, to_y, from_tile_model.tile_type, from_tile_model.tile_direction)
        self.tile_config(x, y, TileType.EMPTY, Direction.RIGHT)

    def tile_config(
        self,
        x: int,
        y: int,
        tile_type: TileType | str | None = None,
        tile_direction: Direction | None = None,
    ) -> None:
        tile_model = self.get_tile_model(x, y)

        if tile_model is None:
            logger.error(f"No tile model at ({x}, {y})")
            return

        if tile_type is not None:
            tile_model.tile_type = TileType.normalize(tile_type)
        if tile_direction is not None:
            tile_model.tile_direction = Direction.normalize(tile_direction)

        events.TileModelChanged(x, y, tile_type, tile_direction)

    def _on_player_tile_action_requested(self, event: events.PlayerTileActionRequested) -> None:
        self.cycle(event.tile_action)

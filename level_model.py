"""LevelModel class to handle level logic and interact with LevelController and LevelView

Created on 2026.02.18
Contributors:
    Romcode
"""

import logging
from pathlib import Path

from enums import Direction, TileActionType, TileType
import events
from level import Level
from tile import Tile

logger = logging.getLogger(__name__)


class LevelModel:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.level = Level.from_path(self.path)

        rows = self.level.layout.splitlines()
        self.width = len(rows[0])
        self.height = len(rows)

        if any(len(row) != self.width for row in rows):
            raise ValueError(f"Mismatched row length in tilemap layout\n{self.level.layout}")

        self.tiles = tuple(Tile(tile_type) for tile_type in self.level.layout.replace("\n", ""))

        events.MoveRequested.connect(self._on_move_requested)

        events.LevelOpened(
            self.level,
            tuple(tile.tile_type_changed for tile in self.tiles),
        )

    def cycle(self, direction: Direction) -> None:
        # TODO: Remove manual movement
        actions = []
        for y in range(self.height):
            for x in range(self.width):
                actions.append(self.get_tile(x, y).get_action())

        for y in range(self.height):
            for x in range(self.width):
                action = actions[y * self.width + x]
                if action is None:
                    continue
                match action.type:
                    case TileActionType.MOVE:
                        # action.direction
                        if direction is None:
                            continue
                        self.move_tile(x, y, direction)
                    case TileActionType.ATTACK:
                        pass
                    case _:
                        pass

    def destroy(self) -> None:
        events.MoveRequested.disconnect(self._on_move_requested)
        events.LevelClosed()

    def get_tile(self, x: int, y: int) -> Tile | None:
        try:
            assert 0 <= x < self.width
            assert 0 <= y < self.height
            return self.tiles[y * self.width + x]
        except (AssertionError, IndexError):
            return None

    def move_tile(self, x: int, y: int, direction: Direction) -> None:
        from_tile = self.get_tile(x, y)
        to_tile = self.get_tile(x + direction.x, y + direction.y)

        if (
            from_tile is not None
            and to_tile is not None
            and to_tile.tile_type.is_walkable
        ):
            logger.debug(
                "Moving tile '%s' from (%i, %i) in direction '%s' ('%s')",
                from_tile.tile_type.name,
                x,
                y,
                direction.name,
                to_tile.tile_type.name,
            )
            to_tile.set_tile_type(from_tile.tile_type)
            from_tile.set_tile_type(TileType.EMPTY)

    def _on_move_requested(self, event: events.MoveRequested) -> None:
        self.cycle(event.direction)

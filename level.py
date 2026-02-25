"""Level class to store level files

Created on 2026.01.28
Contributors:
    Romcode
"""

from __future__ import annotations
from dataclasses import dataclass
import logging
from pathlib import Path
from typing import Iterator

import yaml
from yaml.parser import ParserError

from common import normalize_path
from enums import Direction, TileType
from errors import InvalidLayoutError

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Level:
    PATHS = (
        Path("levels/test.yaml"),
        Path("levels/tutorial.yaml"),
    )
    YAML_FIELDS = (
        "name",
        "pyscript_path",
        "layout",
        "direction_layout",
    )

    name: str = "Missing level name"
    pyscript_path: Path | None = None
    layout: str = ""
    direction_layout: str = ""
    width: int = 0
    height: int = 0

    @classmethod
    def from_path(cls, path: Path) -> Level:
        logger.debug(f"Loading level from '{path}'")

        try:
            with open(path, "r", encoding="utf-8") as file:
                data = yaml.safe_load(file)
        except FileNotFoundError:
            error_message = f"Missing level file at '{path}'"
            logger.error(error_message)
            return cls(error_message)
        except ParserError:
            error_message = f"Failed to parse level from '{path}'"
            logger.error(error_message)
            return cls(error_message)

        constructor_kwargs = {}

        for field in cls.YAML_FIELDS:
            try:
                constructor_kwargs[field] = data.pop(field)
            except KeyError:
                logger.error(f"Missing field '{field}' in '{path}'")

        for field in data:
            logger.warning(f"Found unexpected field '{field}' in '{path}'")

        return cls(**constructor_kwargs)

    def __post_init__(self):
        def raise_dimension_mismatch() -> None:
            raise InvalidLayoutError(
                "Mismatched dimensions in layout\n%s\n and direction layout\n%s",
                self.layout,
                self.direction_layout,
            )

        if self.pyscript_path is not None:
            object.__setattr__(
                self,
                "pyscript_path",
                normalize_path(self.pyscript_path),
            )

        if self.layout == "":
            object.__setattr__(self, "width", 0)
            object.__setattr__(self, "height", 0)

            if self.direction_layout != "":
                raise_dimension_mismatch()

            return

        rows = self.layout.splitlines()
        object.__setattr__(self, "width", len(rows[0]))
        object.__setattr__(self, "height", len(rows))

        if any(len(row) != self.width for row in rows):
            raise InvalidLayoutError(f"Mismatched row length in layout\n{self.layout}")

        if self.direction_layout == "":
            raise_dimension_mismatch()

        direction_rows = self.direction_layout.splitlines()

        if (
            len(direction_rows) != self.height
            or any(len(row) != self.width for row in direction_rows)
        ):
            raise_dimension_mismatch()

    def iter_tile_data(self) -> Iterator[tuple[TileType, Direction]]:
        return (
            (TileType.normalize(type_char), Direction.normalize(direction_char))
            for type_char, direction_char
            in zip(
                self.layout.replace("\n", ""),
                self.direction_layout.replace("\n", ""),
            )
        )

"""Level class to store level files

Created on 2026.01.28
Contributors:
    Romcode
"""

from __future__ import annotations
from dataclasses import dataclass, fields
import logging
from pathlib import Path

import yaml
from yaml.parser import ParserError

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Level:
    PATHS = (
        Path("levels/test.yaml"),
        Path("levels/tutorial.yaml"),
    )

    name: str = "Missing level name"
    pyscript_path: Path | None = None
    layout: str = ""
    direction_layout: str = ""

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

        for field in fields(cls):
            try:
                constructor_kwargs[field.name] = data.pop(field.name)
            except KeyError:
                logger.error(f"Missing field '{field.name}' in '{path}'")

        for key in data:
            logger.warning(f"Found unexpected field '{key}' in '{path}'")

        if "pyscript_path" in constructor_kwargs:
            constructor_kwargs["pyscript_path"] = Path(constructor_kwargs["pyscript_path"])

        return cls(**constructor_kwargs)

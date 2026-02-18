"""Level class to store level files

Created on 2026.01.28
Contributors:
    Romcode
"""

from __future__ import annotations
from dataclasses import dataclass
import logging
from pathlib import Path

import yaml # pip install PyYAML
from yaml.parser import ParserError

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Level:
    PATHS = (
        Path("levels/test.yaml"),
        Path("levels/tutorial.yaml"),
    )

    name: str = ""
    pyscript_path: Path | None = None
    layout: str = "P"

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

        try:
            name = data["name"]
        except KeyError:
            error_message = f"Missing field 'name' in '{path}'"
            logger.error(error_message)
            name = error_message

        try:
            pyscript_path = data["pyscript_path"]
            if pyscript_path is not None:
                pyscript_path = Path(pyscript_path)
        except KeyError:
            logger.error(f"Missing field 'pyscript_path' in '{path}'")
            pyscript_path = None

        try:
            layout = data["layout"]
        except KeyError:
            logger.error(f"Missing field 'layout' in '{path}'")
            layout = "P"

        return cls(name, pyscript_path, layout)

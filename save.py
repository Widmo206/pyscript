"""Save class to manage user save files

Created on 2026.03.07
Contributors:
    Romcode
"""

from __future__ import annotations
from dataclasses import dataclass, field
import logging
from pathlib import Path

import yaml
from yaml.parser import ParserError

from common import message_error

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class LevelScore:
    solution_path: Path
    token_count: int


@dataclass(frozen=True)
class Save:
    level_scores: dict[Path, LevelScore] = field(default_factory=dict)

    @classmethod
    def from_path(cls, path: Path) -> Save:
        logger.debug("Loading save from '%s'", path)

        try:
            with open(path, "r", encoding="utf-8") as file:
                data = yaml.safe_load(file)
        except FileNotFoundError:
            message_error("Missing save file at '%s'", path)
            return cls()
        except ParserError:
            message_error("Failed to parse save from '%s'", path)
            return cls()

        try:
            return cls(data["level_scores"])
        except KeyError:
            message_error("Missing field 'level_scores' in '%s'", path)

        return cls()

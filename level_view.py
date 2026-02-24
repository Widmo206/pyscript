"""LevelView class to manage TileLabels and obey LevelModel

Created on 2026.01.28
Contributors:
    Romcode
"""

import logging
from math import floor
import tkinter as tk

import ttkbootstrap as ttk

import events
from level import Level
from tile_label import TileLabel

logger = logging.getLogger(__name__)


class LevelView(ttk.Frame):
    level: Level
    width: int
    height: int

    grid_frame: ttk.Frame
    tile_labels: list[TileLabel]

    def __init__(
        self,
        master: tk.Misc,
        level: Level,
        **kwargs,
    ) -> None:
        kwargs.setdefault("padding", 64)
        super().__init__(master, **kwargs)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.grid_frame = ttk.Frame(self)
        self.grid_frame.grid()

        self.level = level

        if self.level.layout == "":
            self.width = 0
            self.height = 0
            self.tile_labels = []
        else:
            rows = self.level.layout.splitlines()
            self.width = len(rows[0])
            self.height = len(rows)
            self.tile_labels = []
            for y in range(self.height):
                for x in range(self.width):
                    tile_label = TileLabel(self.grid_frame, rows[y][x])
                    tile_label.grid(column=x, row=y)
                    self.tile_labels.append(tile_label)

            if any(len(row) != self.width for row in rows):
                raise ValueError(f"Mismatched row length in tilemap layout\n{self.level.layout}")

        self.bind("<Configure>", lambda _: self.update_tile_size())

        events.TileChanged.connect(self._on_model_tile_changed)

    def destroy(self) -> None:
        events.TileChanged.disconnect(self._on_model_tile_changed)
        ttk.Frame.destroy(self)

    def get_tile_label(self, x: int, y: int) -> TileLabel | None:
        try:
            return self.tile_labels[y * self.width + x]
        except IndexError:
            return None

    def update_tile_size(self) -> None:
        padding = int(str(self.cget("padding")[0])) # TODO: clean up this weird conversion issue
        tile_size = floor(min(
            (self.winfo_width() - padding * 2) / self.width,
            (self.winfo_height() - padding * 2) / self.height,
        ))

        for tile in self.tile_labels:
            tile.tile_config(tile_size=tile_size)

    def _on_model_tile_changed(self, event: events.TileChanged) -> None:
        tile_label = self.get_tile_label(event.x, event.y)

        if tile_label is None:
            logger.error(f"No tile label at ({event.x}, {event.y})")
            return

        tile_label.tile_config(tile_type=event.tile_type, tile_direction=event.direction)

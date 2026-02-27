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
from matrix import Matrix
from tile_label import TileLabel

logger = logging.getLogger(__name__)


class LevelView(ttk.Frame):
    level: Level

    grid_frame: ttk.Frame
    tile_labels: Matrix[TileLabel]

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

        tile_data_matrix = level.get_tile_data_matrix()
        self.tile_labels = Matrix(
            tile_data_matrix.width,
            tile_data_matrix.height,
            (
                TileLabel(
                    self.grid_frame,
                    tile_data.tile_type,
                    tile_data.tile_direction,
                ) for tile_data in tile_data_matrix
            ),
        )

        for x, y, tile_label in self.tile_labels.iter_xy():
            tile_label.grid(column=x, row=y)

        self.bind("<Configure>", lambda _: self.update_tile_size())

        events.TileDataChanged.connect(self._on_tile_model_changed)

    def destroy(self) -> None:
        events.TileDataChanged.disconnect(self._on_tile_model_changed)
        ttk.Frame.destroy(self)

    def update_tile_size(self) -> None:
        padding = int(str(self.cget("padding")[0])) # TODO: clean up this weird conversion issue
        tile_size = floor(min(
            (self.winfo_width() - padding * 2) / self.level.width,
            (self.winfo_height() - padding * 2) / self.level.height,
        ))

        for tile_label in self.tile_labels:
            tile_label.tile_config(tile_size=tile_size)

    def _on_tile_model_changed(self, event: events.TileDataChanged) -> None:
        try:
            tile_label = self.tile_labels.get(event.x, event.y)
        except IndexError:
            logger.error(f"No tile view at ({event.x}, {event.y})")
            return

        tile_label.tile_config(tile_type=event.tile_type, tile_direction=event.direction)

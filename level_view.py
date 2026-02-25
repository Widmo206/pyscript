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
from tile_view import TileView

logger = logging.getLogger(__name__)


class LevelView(ttk.Frame):
    level: Level

    grid_frame: ttk.Frame
    tile_views: tuple[TileView]

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
        self.tile_views = tuple(
            TileView(self.grid_frame, tile_type, tile_direction)
            for tile_type, tile_direction
            in level.iter_tile_data()
        )
        for i, tile_view in enumerate(self.tile_views):
            tile_view.grid(
                column=i % self.level.width,
                row=i // self.level.width,
            )

        self.bind("<Configure>", lambda _: self.update_tile_size())

        events.TileModelChanged.connect(self._on_tile_model_changed)

    def destroy(self) -> None:
        events.TileModelChanged.disconnect(self._on_tile_model_changed)
        ttk.Frame.destroy(self)

    def get_tile_view(self, x: int, y: int) -> TileView | None:
        try:
            assert 0 <= x < self.level.width
            assert 0 <= y < self.level.height
            return self.tile_views[y * self.level.width + x]
        except (AssertionError, IndexError):
            return None

    def update_tile_size(self) -> None:
        padding = int(str(self.cget("padding")[0])) # TODO: clean up this weird conversion issue
        tile_size = floor(min(
            (self.winfo_width() - padding * 2) / self.level.width,
            (self.winfo_height() - padding * 2) / self.level.height,
        ))

        for tile_view in self.tile_views:
            tile_view.tile_config(tile_size=tile_size)

    def _on_tile_model_changed(self, event: events.TileModelChanged) -> None:
        tile_view = self.get_tile_view(event.x, event.y)

        if tile_view is None:
            logger.error(f"No tile view at ({event.x}, {event.y})")
            return

        tile_view.tile_config(tile_type=event.tile_type, tile_direction=event.direction)

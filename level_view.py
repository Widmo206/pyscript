"""LevelView class to manage TileLabels and obey LevelModel

Created on 2026.01.28
Contributors:
    Romcode
"""

from math import floor
import tkinter as tk

import ttkbootstrap as ttk

import events
from tile_label import TileLabel


class LevelView(ttk.Frame):
    def __init__(
        self,
        master: tk.Misc,
        event: events.LevelOpened,
        **kwargs,
    ) -> None:
        if event.level.layout == "":
            raise ValueError("Tilemap layout cannot be empty")

        self.layout = event.level.layout

        rows = self.layout.splitlines()
        self.width = len(rows[0])
        self.height = len(rows)

        if any(len(row) != self.width for row in rows):
            raise ValueError(f"Mismatched row length in tilemap layout\n{self.layout}")

        kwargs.setdefault("padding", 64)
        super().__init__(master, **kwargs)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        self.grid_frame = ttk.Frame(self)
        self.grid_frame.grid()

        self.bind("<Configure>", lambda _: self.update_tile_size())

        self.tiles = []
        for y in range(self.height):
            for x in range(self.width):
                tile = TileLabel(
                    self.grid_frame,
                    rows[y][x],
                    event.tile_instance_events[y * self.width + x],
                )
                tile.grid(column=x, row=y)
                self.tiles.append(tile)

    def update_tile_size(self) -> None:
        padding = int(str(self.cget("padding")[0])) # TODO: clean up this weird conversion issue
        tile_size = floor(min(
            (self.winfo_width() - padding * 2) / self.width,
            (self.winfo_height() - padding * 2) / self.height,
        ))

        for tile in self.tiles:
            tile.resize(tile_size)

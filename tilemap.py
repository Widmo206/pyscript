"""Tilemap class to manage tiles

Created on 2026.01.28
Contributors:
    Romcode
"""

from dataclasses import dataclass
import tkinter as tk

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

import math
from tile import Tile


@dataclass
class Tilemap:
    master: tk.Misc
    width: int = 16
    height: int = 16

    def __post_init__(self) -> None:
        if self.width < 1 or self.height < 1:
            raise ValueError("Grid dimensions cannot be less than 1x1")

        self.frame = ttk.Frame(self.master)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        
        self.grid_frame = ttk.Frame(self.frame)
        self.grid_frame.grid()

        self.frame.bind("<Configure>", lambda _: self.update_tile_size())

        self.tiles = []
        for x in range(self.width):
            for y in range(self.height):
                tile = Tile(self.grid_frame)
                tile.label.grid(column=x, row=y, sticky=NSEW)
                tile.label.config(text=f"{x};{y}")
                self.tiles.append(tile)

    def update_tile_size(self) -> None:
        tile_size = math.floor(min(
            self.frame.winfo_width() / self.width - self.width,
            self.frame.winfo_height() / self.height - self.height,
        ))

        for tile in self.tiles:
            tile.resize(tile_size)

#         for x in range(self.width):
#             self.grid_frame.columnconfigure(x, minsize=tile_size)
#         for y in range(self.height):
#             self.grid_frame.rowconfigure(y, minsize=tile_size)

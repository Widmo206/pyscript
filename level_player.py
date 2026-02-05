"""LevelPlayer class to link LevelBar, LevelSelect and Tilemap

Created on 2026.02.05
Contributors:
    Romcode
"""

import tkinter as tk

import ttkbootstrap as ttk
import ttkbootstrap.constants as ttkc

from level import Level
from level_bar import LevelBar
from tilemap import Tilemap


class LevelPlayer(ttk.Frame):
    def __init__(self, master: tk.Misc, **kwargs) -> None:
        super().__init__(master, **kwargs)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.tilemap = Tilemap(self, Level.from_path(Level.PATHS[0]).tilemap_layout)
        self.tilemap.grid(column=0, row=0, sticky=ttkc.NSEW)

        self.level_bar = LevelBar(self)
        self.level_bar.level_select_button.config(command=self.open_level_select)
        self.level_bar.grid(column=0, row=1, sticky=ttkc.NSEW)

    def open_level_select(self) -> None:
        self.tilemap.destroy()

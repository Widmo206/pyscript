"""LevelPlayer class that contains LevelController and LevelView

Created on 2026.02.05
Contributors:
    Romcode
"""

import logging
import tkinter as tk

import ttkbootstrap as ttk
import ttkbootstrap.constants as ttkc

import events
from level_controller import LevelController
from level_view import LevelView

logger = logging.getLogger(__name__)


class LevelPlayer(ttk.Frame):
    def __init__(
        self,
        master: tk.Misc,
        event: events.LevelOpened,
        **kwargs,
    ) -> None:
        super().__init__(master, **kwargs)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.level = event.level

        logger.debug(f"Creating level view from layout\n{self.level.layout}")
        self.level_view = LevelView(self, event)
        self.level_view.grid(column=0, row=0, sticky=ttkc.NSEW)

        self.level_controller = LevelController(self)
        self.level_controller.grid(column=0, row=1, sticky=ttkc.NSEW)

"""PyscriptManager class that links PyscriptEditor and PyscriptOutput

Created on 2026.02.08
Contributors:
    Romcode
"""

import logging
import tkinter as tk

import ttkbootstrap as ttk
import ttkbootstrap.constants as ttkc

from pyscript_editor import PyscriptEditor
from pyscript_output import PyscriptOutput

logger = logging.getLogger(__name__)


class PyscriptManager(tk.PanedWindow):
    def __init__(
        self,
        master: tk.Misc,
        style: ttk.Style,
        **kwargs,
    ) -> None:
        kwargs.setdefault("orient", tk.VERTICAL)
        kwargs.setdefault("sashwidth", 8)
        kwargs.setdefault("borderwidth", 0)
        kwargs.setdefault("bg", style.colors.dark)
        super().__init__(master, **kwargs)

        self.pyscript_editor = PyscriptEditor(self, style)
        self.add(self.pyscript_editor)

        self.pyscript_output = PyscriptOutput(self, style)
        self.add(self.pyscript_output)

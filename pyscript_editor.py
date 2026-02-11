"""PyscriptEditor class to manage PyscriptEditorTabs

Created on 2026.01.28
Contributors:
    Romcode
"""

import logging
from pathlib import Path
import tkinter as tk

from pyscript_editor_tab import PyscriptEditorTab
import ttkbootstrap as ttk
import ttkbootstrap.constants as ttkc

logger = logging.getLogger(__name__)


class PyscriptEditor(ttk.Notebook):
    def __init__(
        self,
        master: tk.Misc,
        style: ttk.Style,
        **kwargs,
    ) -> None:
        kwargs.setdefault("padding", 0)
        super().__init__(master, **kwargs)

        self.style = style

    def open_pyscript(self, pyscript_path: Path) -> None:
        logger.debug(f"Creating new PyScript tab '{pyscript_path.name}'")
        self.add(
            PyscriptEditorTab(self, self.style, pyscript_path),
            text=pyscript_path.name,
        )

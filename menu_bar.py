"""MenuBar class to manage pyscript files and select levels

Created on 2026.02.01
Contributors:
    Romcode
"""

from dataclasses import dataclass
import tkinter as tk

import ttkbootstrap as ttk
import ttkbootstrap.constants as ttkc


@dataclass
class MenuBar:
    master: tk.Misc

    def __post_init__(self) -> None:
        self.frame = ttk.Frame(self.master, bootstyle=ttkc.DARK)

        self.file_menu_button = ttk.Menubutton(self.frame, text="File", bootstyle=ttkc.DARK)
        self.file_menu_button.grid(column=0, row=0)

        self.file_menu = tk.Menu(self.file_menu_button)
        self.file_menu.add_command(label="New...", command=None)
        self.file_menu.add_command(label="Open...", command=None)
        self.file_menu.add_command(label="Save", command=None)
        self.file_menu.add_command(label="Save as...", command=None)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=None)
        self.file_menu_button["menu"] = self.file_menu

        self.level_menu_button = ttk.Menubutton(self.frame, text="Level", bootstyle=ttkc.DARK)
        self.level_menu_button.grid(column=1, row=0)

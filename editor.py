"""Editor class for writing pyscript in tkinter

Created on 2026.01.28
Contributors:
    Romcode
"""

import tkinter as tk

import ttkbootstrap as ttk
import ttkbootstrap.constants as ttkc


class Editor:
    def __init__(self, master: tk.Misc) -> None:
        self.frame = ttk.Frame(master)

        self.text = ttk.Text(self.frame, wrap=ttkc.NONE)
        self.text.pack(side=ttkc.LEFT, fill=ttkc.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.frame, orient=ttkc.VERTICAL, command=self.text.yview)
        self.scrollbar.pack(side=ttkc.RIGHT, fill=ttkc.Y)

        self.text.config(yscrollcommand=self.scrollbar.set)

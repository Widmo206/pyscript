"""Editor class for writing pyscript in tkinter

Created on 2026.01.28
Contributors:
    Romcode
"""

import tkinter as tk

import ttkbootstrap as ttk
import ttkbootstrap.constants as ttkc
from ttkbootstrap.widgets.scrolled import ScrolledText


class Editor(ttk.Frame):
    def __init__(self, master: tk.Misc, style: ttk.Style, **kwargs) -> None:
        super().__init__(master, **kwargs)

        self.line_text = tk.Text(self)
        self.line_text.config(
            width=4,
            padx=8,
            highlightthickness=0,
            state=ttkc.DISABLED,
            bg=style.colors.primary,
            fg=style.colors.secondary,
            font=("Consolas", 11),
        )
        self.line_text.tag_config("active_line", foreground=style.colors.info)
        self.line_text.pack(side=ttkc.LEFT, fill=ttkc.Y)

        self.scrolled_text = ScrolledText(self, hbar=True, autohide=True, padding=0)
        self.scrolled_text.pack(side=ttkc.LEFT, fill=ttkc.BOTH, expand=True)

        self.text = self.scrolled_text.text
        self.text.configure(
            bg=style.colors.bg,
            highlightthickness=0,
            font=("Consolas", 11),
        )

        self.text.config(yscrollcommand=self._on_text_scroll)
        self.scrolled_text.vbar.config(command=self._on_scrollbar)

        self.text.bind("<<Modified>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)
        self.text.bind("<KeyRelease>", self._on_change)
        self.text.bind("<ButtonRelease-1>", self._on_change)
        self.text.bind("<FocusIn>", self._on_focus_change)
        self.text.bind("<FocusOut>", self._on_focus_change)

        self._update_line_numbers()

    def _on_text_scroll(self, *args):
        self.scrolled_text.vbar.set(*args)
        self.line_text.yview_moveto(args[0])

    def _on_scrollbar(self, *args):
        self.text.yview(*args)
        self.line_text.yview(*args)

    def _on_change(self, event=None):
        self.text.edit_modified(False)
        self._update_line_numbers()

    def _on_focus_change(self, event=None):
        self._update_line_numbers()

    def _update_line_numbers(self):
        first, _ = self.line_text.yview()
        self.line_text.config(state="normal")
        self.line_text.delete("1.0", "end")

        line_count = int(self.text.index("end-1c").split(".")[0])
        numbers = "\n".join(str(i).rjust(4) for i in range(1, line_count + 1))
        self.line_text.insert("1.0", numbers)

        if self.text.focus_get() == self.text:
            current_line = int(self.text.index("insert").split(".")[0])
            self.line_text.tag_add(
                "active_line",
                f"{current_line}.0",
                f"{current_line}.end",
            )

        self.line_text.config(state="disabled")
        self.line_text.yview_moveto(first)

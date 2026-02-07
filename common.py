"""Common classes and functions used by different modules

Created on 2026.02.07
Contributors:
    Romcode
"""

import tkinter as tk
from typing import Callable


def bind_recursive(
    widget: tk.Widget,
    sequence: str | None = None,
    func: Callable | None = None,
    add: str | bool | None = None,
) -> None:
    """Same as Widget.bind, but affects all children recursively."""
    widget.bind(sequence, func, add)
    for child in widget.winfo_children():
        bind_recursive(child, sequence, func, add)

"""Interface class containing all tk elements

Created on 2026.02.04
Contributors:
    Romcode
"""

import logging
import tkinter as tk

import ttkbootstrap as ttk
import ttkbootstrap.constants as ttkc

import events
from level_manager import LevelManager
from menu_bar import MenuBar
from pyscript_manager import PyscriptManager

logger = logging.getLogger(__name__)


class Interface(ttk.Window):
    LEVEL_COMPLETE_POPUP_TITLE = "Level complete"
    LEVEL_COMPLETE_POPUP_HEADER = "Level complete!"
    LEVEL_COMPLETE_POPUP_SIZE = (440, 320)

    main_frame: ttk.Frame
    menu_bar: MenuBar
    margin_frame: ttk.Frame
    paned_window: tk.PanedWindow
    pyscript_manager: PyscriptManager
    level_manager: LevelManager
    level_complete_popup: tk.Toplevel | None

    def __init__(self, **kwargs) -> None:
        kwargs.setdefault("title", "PyScript")
        kwargs.setdefault("themename", "darkly")
        super().__init__(**kwargs)

        self.geometry("1280x720")
        self.state("zoom")

        self.style.colors.set("primary", "#191919")
        self.style.layout("TNotebook", [])

        self.main_frame = ttk.Frame(self)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.pack(anchor=ttkc.CENTER, fill=ttkc.BOTH, expand=True)

        self.menu_bar = MenuBar(self.main_frame)
        self.menu_bar.grid(column=0, row=0, sticky=ttkc.NSEW)

        self.margin_frame = ttk.Frame(self.main_frame, bootstyle=ttkc.DARK)
        self.margin_frame.columnconfigure(0, minsize=8)
        self.margin_frame.columnconfigure(1, weight=1)
        self.margin_frame.columnconfigure(2, minsize=8)
        self.margin_frame.rowconfigure(0, weight=1)
        self.margin_frame.rowconfigure(2, minsize=8)
        self.margin_frame.grid(column=0, row=1, sticky=ttkc.NSEW)

        self.paned_window = tk.PanedWindow(
            self.margin_frame,
            orient=ttkc.HORIZONTAL,
            sashwidth=8,
            borderwidth=0,
            bg=self.style.colors.dark,
        )
        self.paned_window.grid(column=1, row=0, sticky=ttkc.NSEW)

        self.pyscript_manager = PyscriptManager(self.paned_window, self.style)
        self.paned_window.add(self.pyscript_manager)

        self.level_manager = LevelManager(self.paned_window)
        self.paned_window.add(self.level_manager)
        self.level_complete_popup = None

        self.paned_window.paneconfig(self.level_manager, minsize=500)

        self.update_idletasks()
        self.paned_window.sash_place(0, int(self.paned_window.winfo_width() * 0.5), 0)
        self.pyscript_manager.sash_place(0, 0, int(self.pyscript_manager.winfo_height() * 0.75))

        events.ToggleFullscreenRequested.connect(lambda _: self.toggle_fullscreen())
        events.LevelComplete.connect(self._on_level_complete)
        events.LevelClosed.connect(lambda _: self._close_level_complete_popup())

    def toggle_fullscreen(self) -> None:
        new_mode = not self.attributes("-fullscreen")
        logger.debug(f"Setting fullscreen mode to {new_mode}")
        self.attributes("-fullscreen", new_mode)

    def _close_level_complete_popup(self) -> None:
        if self.level_complete_popup is None:
            return

        if self.level_complete_popup.winfo_exists():
            self.level_complete_popup.destroy()
        self.level_complete_popup = None

    def _on_popup_level_select(self) -> None:
        self._close_level_complete_popup()
        events.LevelSelectButtonPressed()

    def _on_popup_restart(self) -> None:
        self._close_level_complete_popup()
        events.RestartRequested()

    def _on_level_complete(self, event: events.LevelComplete) -> None:
        self._close_level_complete_popup()

        # TODO: Rework this slop

        popup = tk.Toplevel(self)
        popup.title(self.LEVEL_COMPLETE_POPUP_TITLE)
        popup.transient(self)
        popup.resizable(False, False)
        popup.protocol("WM_DELETE_WINDOW", self._close_level_complete_popup)
        popup.bind("<Escape>", lambda _: self._close_level_complete_popup())
        self.level_complete_popup = popup

        width, height = self.LEVEL_COMPLETE_POPUP_SIZE
        x = self.winfo_rootx() + (self.winfo_width() - width) // 2
        y = self.winfo_rooty() + (self.winfo_height() - height) // 2
        popup.geometry(f"{width}x{height}+{x}+{y}")

        main_frame = ttk.Frame(popup, padding=20)
        main_frame.pack(fill=ttkc.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        header = ttk.Label(
            main_frame,
            text=self.LEVEL_COMPLETE_POPUP_HEADER,
            anchor=ttkc.CENTER,
            font=("Segoe UI", 18),
            bootstyle=(ttkc.SUCCESS, ttkc.INVERSE),
            padding=(0, 10),
        )
        header.grid(column=0, row=0, sticky=ttkc.EW)

        stats_frame = ttk.Frame(main_frame, padding=(0, 12))
        stats_frame.grid(column=0, row=1, sticky=ttkc.NSEW)
        stats_frame.columnconfigure(1, weight=1)

        script_name = (
            "N/A"
            if event.level.pyscript_path is None
            else event.level.pyscript_path.name
        )
        stats = (
            ("Level", event.level.name),
            ("Steps", str(event.step_count)),
            ("Grid", f"{event.level.width} x {event.level.height}"),
            ("Script", script_name),
        )

        for row, (label, value) in enumerate(stats):
            ttk.Label(
                stats_frame,
                text=f"{label}:",
                anchor=ttkc.W,
                font=("Segoe UI", 11, "bold"),
            ).grid(column=0, row=row, sticky=ttkc.W, pady=4, padx=(0, 12))
            ttk.Label(
                stats_frame,
                text=value,
                anchor=ttkc.W,
                font=("Segoe UI", 11),
            ).grid(column=1, row=row, sticky=ttkc.W, pady=4)

        buttons = ttk.Frame(main_frame)
        buttons.grid(column=0, row=2, sticky=ttkc.E)
        ttk.Button(
            buttons,
            text="Close",
            command=self._close_level_complete_popup,
            bootstyle=ttkc.SECONDARY,
        ).grid(column=0, row=0, padx=(0, 8))
        ttk.Button(
            buttons,
            text="Level select",
            command=self._on_popup_level_select,
            bootstyle=ttkc.PRIMARY,
        ).grid(column=1, row=0, padx=(0, 8))
        ttk.Button(
            buttons,
            text="Restart",
            command=self._on_popup_restart,
            bootstyle=ttkc.SUCCESS,
        ).grid(column=2, row=0)

        popup.grab_set()
        popup.focus_set()


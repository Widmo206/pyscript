"""TileLabel class for display

Created on 2026.01.28
Contributors:
    Romcode
"""

import logging
from PIL import ImageTk, Image
import tkinter as tk

import ttkbootstrap as ttk
import ttkbootstrap.constants as ttkc

from tile_action import TileAction
from enums import TileActionType, Direction, TileType
from errors import UnknownTileTypeError

logger = logging.getLogger(__name__)


class TileLabel(ttk.Label):
    MIN_SIZE = 32
    PADDING_RATIO = 0.05

    def __init__(
        self,
        master: tk.Misc,
        tile_type: TileType | str = TileType.EMPTY,
        **kwargs,
    ) -> None:
        kwargs.setdefault("borderwidth", 0)
        super().__init__(master, **kwargs)

        self.tile_type: TileType | None = None
        self.image_tk: ImageTk.PhotoImage | None = None

        self.set_tile_type(tile_type)

    def get_action(self) -> TileAction | None:
        if self.tile_type == TileType.PLAYER:
            # TODO: Implement action choice
            return TileAction(TileActionType.MOVE, Direction.UP)
        else:
            return None

    def resize(self, tile_size: int) -> None:
        tile_size = max(tile_size, self.MIN_SIZE)

        if tile_size < 1:
            raise ValueError(f"TileLabel size ({tile_size}) cannot be less than 1")

        image_size = round(tile_size * (1 - self.PADDING_RATIO))
        pad_size = round(tile_size * self.PADDING_RATIO / 2)
        self.image_tk = ImageTk.PhotoImage(self.tile_type.image.resize(
            (image_size, image_size),
            Image.Resampling.LANCZOS,
        )) if self.tile_type.image else None
        self.configure(image=self.image_tk, padding=pad_size)

    def set_tile_type(self, tile_type: TileType | str) -> None:
        if isinstance(tile_type, str):
            try:
                self.tile_type = TileType(tile_type)
            except UnknownTileTypeError:
                logger.error(f"No tile type matching character '{self.tile_type}'")
                self.tile_type = TileType.EMPTY
        else:
            self.tile_type = tile_type

        self.image_tk = ImageTk.PhotoImage(self.tile_type.image) if self.tile_type.image else None
        self.config(image=self.image_tk)

"""Centralized location for easy error access

Created on 2026.01.31
Contributors:
    Romcode
    Widmo
"""

from yaml.parser import ParserError


class UnknownTileTypeError(ValueError):
    """Raised when a tile is asked to convert a character to a type that doesn't exist."""
    pass


class UnknownTokenError(ValueError):
    """Raised when the Parser finds a token that is broken or doesn't exist."""
    pass

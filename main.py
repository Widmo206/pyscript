"""Pyscript - a coding learning game

Created on 2026.01.28
Contributors:
    Romcode
"""

from interface import Interface


def main() -> None:
    Interface()


if __name__ == "__main__":
    main()
else:
    raise RuntimeError("main.py should not be imported")

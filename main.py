"""Pyscript - a coding learning game

Created on 2026.01.28
Contributors:
    Romcode
"""

import logging

from interface import Interface


def main() -> None:
    interface = Interface()
    interface.mainloop()


if __name__ == "__main__":
    open("latest.log", "w").close()
    logging.basicConfig(
        filename='latest.log',
        level=logging.DEBUG,
        format="%(asctime)s.%(msecs)03d | %(levelname)-7s | %(name)-13s | %(message)s",
        datefmt='%Y.%m.%d %H:%M:%S',
    )
    # Needed because PIL was flooding the logs
    logging.getLogger('PIL.PngImagePlugin').setLevel(logging.WARNING)

    main()
else:
    raise RuntimeError("main.py should not be imported")

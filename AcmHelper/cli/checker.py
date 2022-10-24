from .config import *


class Checker:
    def __init__(self, cnt: int):
        self.cnt = cnt
        self._in: dict[str, Path] = {}
        self._out: dict[str, Path] = {}

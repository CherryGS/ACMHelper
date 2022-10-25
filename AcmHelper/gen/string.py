from random import randint, sample
from typing import Callable


str_sigma = [
    "abcdefghijklmnopqrstuvwxyz",
    "abcdefghijklmnopqrstuvwxyz".upper(),
    "0123456789",
]


class String:
    def __init__(self, _type: str | None = "l", sigma: str | None = None) -> None:
        """
        _type : 字符集
            l -> lower
            u -> upper
            n -> number
            及其组合
        sigma : 自定义字符集 , 与 _type 求并
        """
        s: set[str] = set()
        if _type is not None:
            for i in _type:
                r = 0
                if i == "l":
                    r = 0
                elif i == "u":
                    r = 1
                else:
                    r = 2

                s = s | {_ for _ in str_sigma[r]}
        if sigma is not None:
            s = s | {_ for _ in sigma}
        self.sigma = "".join(s)

    def _random(self, n: int, sigma: str):
        l = len(sigma)
        return "".join([sigma[randint(1, l) - 1] for _ in range(n)])

    def _paral(self, n: int, lim: int | None = None):
        if lim is None:
            lim = randint(1, len(self.sigma))
        lim = min(lim, len(self.sigma))
        lim = max(1, lim)
        s = "".join(sample(self.sigma, lim))
        c = self._random(int(n / 2), s)
        if n % 2 == 1:
            return c + self._random(1, s) + c[::-1]
        else:
            return c + c[::-1]

    def _rand(self, n: int, lim: int | None = None):
        if lim is None:
            lim = randint(1, len(self.sigma))
        lim = min(lim, len(self.sigma))
        lim = max(1, lim)
        s = "".join(sample(self.sigma, lim))
        return self._random(n, s)

    def gen(self, n: int):
        l: list[Callable] = [self._rand, self._paral]
        c = sample(l, 1)[0]
        return c(n)

    def __call__(self, n: int):
        return self.gen(n)

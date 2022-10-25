from typing import Callable
from .base_graph import BaseGraph
from random import randint, sample, random


class Tree(BaseGraph):
    def __init__(self, n: int, weighed: bool = False) -> None:
        """Tree initialization. Root is 1.

        Args:
            n (int): vertex number
            weighed (bool, optional): weighted graph. Defaults to False.
        """
        super().__init__(n, n - 1, True, weighed)

    def _random(self, s: int, t: int):
        """random .

        Args:
            s (int): start
            t (int): end
        """
        if s > t:
            return
        for v in range(s, t + 1):
            u = randint(1, v - 1)
            self.add_edge(u, v)

    def _random_v1(self, r: int, s: int, t: int, dep: int | None = None):
        """random tree.

        Args:
            r (int): root
            s (int): start
            t (int): end
            mxdep (int): max dep
        """
        if s > t:
            return
        if dep is None:
            dep = randint(2, t - s + 2)
        c0: set[tuple[int, int]] = {(r, 1)}
        for i in range(s, t + 1):
            c = sample(c0, 1)[0]
            self.add_edge(c[0], i)
            if c[1] + 1 < dep:
                c0.add((i, c[1] + 1))

    def _random_v2(self, r: int, s: int, t: int, agg: float | None = None):
        """random tree.

        Args:
            r (int): root
            s (int): start
            t (int): end
            agg (float): degree of aggregation
        """
        if s > t:
            return
        if agg is None:
            agg = random()
        c0 = [[] for _ in range(t - s + 2)]
        c0[0].append(r)
        for i in range(s, t + 1):
            j = 0
            while j < t - s + 1 and random() > agg and len(c0[j + 1]) > 0:
                j += 1
            c = sample(c0[j], 1)[0]
            self.add_edge(c, i)
            c0[j + 1].append(i)

    def _binary(self, r: int, s: int, t: int, bal: float | None = None):
        """binary tree.

        Args:
            r (int): root
            s (int): the previous vertex of the starting
            t (int): end
            bal (float): probability of selecting the left side
        """
        if s > t:
            return
        if bal is None:
            bal = random()
        c0 = {r}
        c1 = set()
        for i in range(s, t + 1):
            if (random() <= bal or len(c1) == 0) and len(c0) > 0:
                c = sample(c0, 1)[0]
                c1.add(c)
                c0.remove(c)
            else:
                c = sample(c1, 1)[0]
                c1.remove(c)
            c0.add(i)
            self.add_edge(c, i)

    def gen_edge(self):
        """Tree generation.

        Args:
            c (TreeConfig, optional): Generation config. Defaults to TreeConfig().
        """

        l: list[Callable] = [self._binary, self._random_v1, self._random_v2]
        c = sample(l, 1)[0]
        c(1, 2, self.n)

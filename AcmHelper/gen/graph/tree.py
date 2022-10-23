from dataclasses import dataclass
from .base_graph import BaseGraph
from random import randint, sample, random


@dataclass
class TreeConfig:
    chain: float = 0
    flower: float = 0
    foot: float = 0


class Tree(BaseGraph):
    def __init__(self, n: int, weighed: bool = False) -> None:
        """Tree initialization. Root is 1.

        Args:
            n (int): vertex number
            weighed (bool, optional): weighted graph. Defaults to False.
        """
        super().__init__(n, n - 1, True, weighed)

    def _random(self, s: int, t: int):
        """random tree.

        Args:
            s (int): the previous vertex of the starting
            t (int): end
        """
        for v in range(s + 1, t + 1):
            u = randint(1, v - 1)
            self.add_edge(u, v)

    def _chain(self, s: int, t: int):
        """chain.

        Args:
            s (int): the previous vertex of the starting
            t (int): end
        """
        for v in range(s + 1, t + 1):
            u = v - 1
            self.add_edge(u, v)

    def _flower(self, s: int, t: int):
        """flower

        Args:
            s (int): the previous vertex of the starting
            t (int): end
        """
        u = randint(1, s)
        for v in range(s + 1, t + 1):
            self.add_edge(u, v)

    def _foot(self, s: int, t: int):
        """Graph generated as follows.
        First generate a chain.
        Then add a son to each vertex in the chain.

        Args:
            s (int): the previous vertex of the starting
            t (int): end
        """
        l = t - s
        for i in range(s + 1, s + int(l / 2 + 0.5) + 1):
            self.add_edge(i - 1, i)
        r = s + int(l / 2 + 0.5) + 1
        for i in range(s, r):
            if r <= t:
                self.add_edge(i, r)
                r = r + 1
            else:
                break

    def _binary(self, s: int, t: int):
        """binary tree.

        Args:
            s (int): the previous vertex of the starting
            t (int): end
        """
        e = {s: 0}
        for i in range(s + 1, t + 1):
            r = sample(e.keys(), 1)[0]
            self.add_edge(r, i)
            e[i] = 0
            e[r] += 1
            if e[r] == 2:
                e.pop(r)

    def gen_edge(self, c: TreeConfig = TreeConfig()):
        """Tree generation.

        Args:
            c (TreeConfig, optional): Generation config. Defaults to TreeConfig().
        """

        n = self.n
        sum = 1

        # chain
        self._chain(sum, sum + int(c.chain * n))
        sum += int(c.chain * n)

        # flower
        self._flower(sum, sum + int(c.flower * n))
        sum += int(c.flower * n)

        # binary
        self._binary(sum, sum + int(c.flower * n))
        sum += int(c.flower * n)

        # foot
        self._foot(sum, sum + int(c.flower * n))
        sum += int(c.flower * n)

        # random
        self._random(sum, n)

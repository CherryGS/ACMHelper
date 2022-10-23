from random import randint, sample
from .base_graph import BaseGraph


class DAG(BaseGraph):
    def __init__(self, n: int, m: int, weighed: bool = False) -> None:
        """DAG initialization.

        Args:
            n (int): vertex number
            m (int): edge number
            weighed (bool, optional): weighted graph. Defaults to False.

        Raises:
            ValueError: Improper number of vertex or edge.
        """
        if n * (n - 1) < m * 2 or n < 0 or m < 0:
            raise ValueError("Improper number of vertex or edge.")
        super().__init__(n, m, True, weighed)

    def gen_edge(self):
        """DAG generation."""
        n = self.n
        m = self.m
        for i in range(2, n + 1):
            mx = min(m - n + i, i - 1)
            mn = max(1, m - int((n - 1) * n / 2) + int((i - 1) * i / 2))
            cnt = randint(mn, mx)
            m -= cnt
            f = sample(range(i - 1), cnt)
            for j in f:
                self.add_edge(j + 1, i)

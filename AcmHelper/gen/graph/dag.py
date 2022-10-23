from random import randint, sample
from .base_graph import BaseGraph


class DAG(BaseGraph):
    def __init__(self, n: int, m: int, weighed: bool = False) -> None:
        if n * (n - 1) < m * 2:
            raise ValueError("边数过多或点数过少")
        super().__init__(n, m, True, weighed)

    def gen_edge(self):
        """保证联通"""
        n = self.n
        sum = self.m
        for i in range(2, n + 1):
            mx = min(sum - n + i, i - 1)
            mn = max(1, sum - int((n - 1) * n / 2) + int((i - 1) * i / 2))
            cnt = randint(mn, mx)
            sum -= cnt
            f = sample(range(i - 1), cnt)
            for j in f:
                self.add_edge(j + 1, i)

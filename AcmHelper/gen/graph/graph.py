from random import randint, sample

from .base_graph import BaseGraph


class Graph(BaseGraph):
    def __init__(
        self, n: int, m: int, directed: bool = False, weighed: bool = False
    ) -> None:
        if n * (n - 1) < m * 2 and directed == False:
            raise ValueError("边数过多或点数过少")
        if n * (n - 1) < m * 2 * 2 and directed == True:
            raise ValueError("边数过多或点数过少")
        super().__init__(n, m, directed, weighed)

    def gen_edge(self):
        """保证联通"""
        sum = self.m * 2 * (2 if self.directed else 1)
        n = self.n
        return NotImplementedError()

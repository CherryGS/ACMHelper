from random import randint, sample

from .base_graph import BaseGraph


class Graph(BaseGraph):
    def __init__(
        self, n: int, m: int, directed: bool = False, weighed: bool = False
    ) -> None:
        if n < 0 or m < 0:
            raise ValueError("Improper number of vertex or edge.")
        if n * (n - 1) < m * 2 and directed == False:
            raise ValueError("Improper number of vertex or edge.")
        if n * (n - 1) < m * 2 * 2 and directed == True:
            raise ValueError("Improper number of vertex or edge.")
        super().__init__(n, m, directed, weighed)

    def gen_edge(self):
        n = self.n
        m = self.m
        if self.directed:
            for i in range(1, n + 1):
                mx = min(m - n + i, n - 1)
                mn = max(int(i != 1), m - (n - 1) * (n - i))
                cnt = randint(mn, mx)
                m -= cnt
                c1 = randint(max(int(i != 1), cnt - n + i), min(cnt, i - 1))
                f = list()
                if c1 != 0:
                    f += sample(range(1, i), c1)
                if cnt - c1 != 0:
                    f += sample(range(i + 1, n + 1), cnt - c1)
                for j in f:
                    self.add_edge(i, j)
        else:
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

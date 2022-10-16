from .base_graph import BaseGraph
from random import randint, sample, random


class Tree(BaseGraph):
    def __init__(self, n: int, weighed: bool = False) -> None:
        super().__init__(n, n - 1, True, weighed)

    def _random(self, s: int, t: int):
        """[s+1, t] 纯随机生成 , 期望树高 log n"""
        for v in range(s + 1, t + 1):
            u = randint(1, v - 1)
            self.add_edge(u, v)

    def _chain(self, s: int, t: int):
        """[s+1, t] 生成链"""
        for v in range(s + 1, t + 1):
            u = v - 1
            self.add_edge(u, v)

    def _flower(self, s: int, t: int):
        """[s+1, t] 生成菊花"""
        u = randint(1, s)
        for v in range(s + 1, t + 1):
            self.add_edge(u, v)

    def _foot(self, s: int, t: int):
        """
        [s+1, t] 按如下规则生成
        先生成一条链 , 再在每个节点挂上一个额外的节点
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
        """[s+1, t] 生成二叉树"""
        e = {s: 0}
        for i in range(s + 1, t + 1):
            r = sample(e.keys(), 1)[0]
            self.add_edge(r, i)
            e[i] = 0
            e[r] += 1
            if e[r] == 2:
                e.pop(r)

    def gen_edge(
        self,
        _type: int = 0,
        chain: float = -1,
        flower: float = -1,
    ):
        """保证联通
        _type :
            0 -> 完全随机

            1 -> 菊花 + 链 + 随机

            2 -> 随机二叉树

            3 -> _foot
        """
        if len(self.edgeList) != 0:
            raise ValueError("图已生成")
        n = self.n
        if _type == 0:
            self._random(1, n)
        elif _type == 1:
            if chain + flower > 1:
                raise ValueError("概率大于 1")
            if chain < 0 or flower < 0:
                chain = random()
                flower = random() * (1 - chain)
            n1 = int(n * chain)
            n2 = int(n * flower)
            self._flower(1, n1)
            self._chain(n1, n2 + n1)
            self._random(n1 + n2, n)
        elif _type == 2:
            self._binary(1, n)
        elif _type == 3:
            self._foot(1, n)
        else:
            raise NotImplementedError()

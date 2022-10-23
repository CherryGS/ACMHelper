from pathlib import Path
from typing import Iterator
from typing_extensions import Self
from graphviz import Digraph, Graph
from random import randint

type_weight = float | int

class Edge:
    def __init__(self, u: int, v: int, w: type_weight = 0) -> None:
        """
        u : 起点
        v : 终点
        w : 权值参数
        """
        self.u = u
        self.v = v
        self.w = w
        self.nxt: Self = self  # 前向星的下一个节点
    
    def __repr__(self) -> str:
        return f"{self.u} {self.v} {self.w}"


class BaseGraph:
    """所有无自环无重边的图的基本架构"""
    def __init__(self, n: int, m: int, directed: bool = False, weighed: bool = False) -> None:
        """
        节点编号从 1 开始
        n : 节点个数
        m : 边个数
        directed : 是否是有向图(仅决定 render 工作方式)
        weighed : 是否是赋权图(仅决定 render 工作方式)
        """
        self.n = n
        self.m = m
        self.weighed = weighed
        self.directed = directed
        self.edgeList: list[Edge] = []

    def _add_edge(self, u: int, v: int, w: type_weight = 0):
        self.edgeList.append(Edge(u, v, w))

    def add_edge(self, u: int, v: int, w: type_weight = 0):
        self._add_edge(u, v, w)

    def iterator_edge(self) -> Iterator[Edge]:
        return self.edgeList.__iter__()
    
    def render(self, path: Path|str = '.'):
        if self.n > 100 or self.m > 200:
            print("图过大 , 不生成")
            return
        if type(path) == str:
            path = Path(path)
        graph = Digraph if self.directed else Graph
        dot = graph('Graph', 'Rendered by Graphviz')
        for i in range(1, self.n+1):
            dot.node(str(i))
        if self.weighed:
            for i in self.edgeList:
                dot.edge(str(i.u), str(i.v), str(i.w))
        else:
            for i in self.edgeList:
                dot.edge(str(i.u), str(i.v))
        dot.render(directory=path, format='png')
    
    def gen_weight(self, min_value: int = 0, max_value: int = 1):
        if self.weighed:
            for i in self.edgeList:
                i.w = randint(min_value, max_value)
    
    def gen_edge(self):
        raise NotImplementedError()
            
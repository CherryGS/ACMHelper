from pathlib import Path
from typing import Iterator
from typing_extensions import Self
from graphviz import Digraph, Graph
from random import randint

type_weight = float | int

class Edge:
    def __init__(self, u: int, v: int, w: type_weight = 0) -> None:
        """Edge initialization

        Args:
            u (int): start
            v (int): end
            w (type_weight, optional): edge weight. Defaults to 0.
        """
        self.u = u
        self.v = v
        self.w = w
    
    def __repr__(self) -> str:
        return f"{self.u} {self.v} {self.w}"


class BaseGraph:
    """A (weakly) connected graph with no self-loop and multiple edge"""
    def __init__(self, n: int, m: int, directed: bool = False, weighed: bool = False) -> None:
        """
        ! DO NOT USE IT DIRECTLY.
        
        Graph initialization. Vertex start from 1.

        Args:   
            n (int): vertex num
            m (int): edge num
            directed (bool, optional): directed graph. Defaults to False.
            weighed (bool, optional): weighted graph. Defaults to False.
            
        Raises:
            ValueError: Improper number of vertex or edge.
        """
        if n > m+1:
            raise ValueError("Improper number of vertex or edge.")
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
    
    def render(self, path: Path|str = '.', name: str = 'Graph'):
        """Render the graph using Graphviz.

        Args:
            path (Path | str, optional): image output path. Defaults to '.'.

        Raises:
            ValueError: limit the size of the graph.
        """
        if self.n > 100 or self.m > 200:
            raise ValueError("The graph is too big.")
        if type(path) == str:
            path = Path(path)
        graph = Digraph if self.directed else Graph
        dot = graph(name, 'Rendered by Graphviz')
        for i in range(1, self.n+1):
            dot.node(str(i))
        if self.weighed:
            for i in self.edgeList:
                dot.edge(str(i.u), str(i.v), str(i.w))
        else:
            for i in self.edgeList:
                dot.edge(str(i.u), str(i.v))
        dot.render(directory=path, format='png', filename=name)
    
    def gen_weight(self, min_value: int = 0, max_value: int = 1):
        """Generate edge weight between [min_value,max_value]

        Args:
            min_value (int, optional): min value. Defaults to 0.
            max_value (int, optional): max value. Defaults to 1.
            
        Raises:
            ValueError: Graph is already generated.
        """
        if self.weighed:
            for i in self.edgeList:
                i.w = randint(min_value, max_value)
    
    def gen_edge(self):
        if len(self.edgeList) != 0:
            raise ValueError("Graph is already generated.")
        raise NotImplementedError()
            
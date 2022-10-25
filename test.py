from AcmHelper import gen
from rich import inspect

tree = gen.Tree(10, weighed=True)
tree.gen_edge()
tree.gen_weight(1, 10)
inspect(tree)

dag = gen.DAG(10, 20, weighed=False)
dag.gen_edge()
inspect(dag)

graph = gen.Graph(10, 20, weighed=True)
graph.gen_edge()
graph.gen_weight(-10, -1)
inspect(graph)

gen_str = gen.String(_type="lun", sigma="!@#$%^&*()")
inspect(gen_str(50))

try:
    tree.render(name='tree')
    dag.render(name='dag')
    graph.render(name='graph')
except:
    pass
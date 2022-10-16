from gen import Tree, DAG

t = DAG(10, 10)
t.gen_edge()
t.gen_weight(min_value=-10000, max_value=10000)
t.render()

from AcmHelper import gen

t = gen.Graph(20, 60, True)
t.gen_edge()
# t.gen_weight(min_value=-10000, max_value=10000)
t.render()

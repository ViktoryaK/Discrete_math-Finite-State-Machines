from graphviz import Digraph
dot = Digraph(comment='A simple Graph')
dot.node('A', 'Cloudy')
dot.node('B', 'Sunny')
dot.node('C', 'Rainy')
dot.edges(['AB', 'AC'])
dot.edge('B', 'C', constraint='false')
dot.format = 'png'
dot.render('my_graph', view=False)
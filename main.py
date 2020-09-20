import sys
from graphviz import Digraph
from graphviz import Source


def delete_comments(f):
    return f


if __name__ == '__main__':
    # str: str = sys.argv[1]
    # print(str)

    dot = Digraph(comment='The Round Table')
    dot.node('A', 'King Arthur')
    dot.node('B', 'Sir Bedevere the Wise')
    dot.node('L', 'Sir Lancelot the Brave')

    dot.edges(['AB', 'AL'])
    dot.edge('B', 'L', constraint='false')

    s = Source(dot.source, filename="ddg.gv", format="png")
    s.view()
    # f = open(str, 'r')
    # print(f.read())
    # f_without_comments = delete_comments(f)

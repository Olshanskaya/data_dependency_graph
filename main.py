from __future__ import print_function
import sys
from graphviz import Digraph
from graphviz import Source




sys.path.extend(['.', '..'])

from pycparser import c_parser, c_ast



def add_to_graph_assignment(dot, pairs, operation):
    # print(operation)
    return dot, pairs


def add_to_graph_decl(dot, pairs, operation):
    str_to_dot = ""
    print(operation)
    name_val = operation.name
    init_value = operation.init
    if init_value is None:
        str_to_dot = name_val + " = ?"
    else:
        str_to_dot = name_val + " = " + init_value.value

    pairs[name_val] = name_val + "1"
    dot.node(pairs[name_val], str_to_dot, shape='box')
    return dot, pairs


def add_to_graph_return(dot, pairs, operation):
    # print(operation)
    return dot, pairs


if __name__ == '__main__':
    # результирующий граф
    dot = Digraph()

    # список пар с именем переменной и соответствующим именем блока,
    # соответствующему последнему изменению данной переменной
    pairs = dict()

    # читаем из файла код программы
    str: str = sys.argv[1]
    f = open(str, 'r')
    text = f.read()

    text = """
     int get_change(int m) {
        int n = 0;
        n = m / 10;    
        m %= 10;
        n += m / 5;
        m %= 5;
        int c;
        n += m;
        return n;
    }
        """

    parser = c_parser.CParser()
    ast = parser.parse(text, filename='<none>')
    nodes = ast.children()[0][1]
    decl = nodes.children()[0][1]
    FuncDecl = decl.children()[0][1]
    pl = FuncDecl.children()[0][1]
    ParamList = pl.children()
    n = len(ParamList)
    fun_decl = decl.name + "("
    for i in range(n):
        TypeDecl = ParamList[i][1]
        if TypeDecl.name == None:
            fun_decl = fun_decl + ")"
            break
        declname = TypeDecl.name
        if i == n - 1:
            fun_decl = fun_decl + declname + ") "
        else:
            fun_decl = fun_decl + declname + ", "
        pairs[declname] = 'fun_decl'

    dot.node('fun_decl', fun_decl)
    print(pairs)

    # print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
    compound = nodes.children()[1][1]
    operations = compound.children()
    n = len(operations)
    for i in range(n):
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
        next_op = operations[i][1]
        if isinstance(next_op, c_ast.Assignment):
            dot, pairs = add_to_graph_assignment(dot, pairs, next_op)
        elif isinstance(next_op, c_ast.Decl):
            dot, pairs = add_to_graph_decl(dot, pairs, next_op)
        elif isinstance(next_op, c_ast.Return):
            dot, pairs = add_to_graph_return(dot, pairs, next_op)

        print(pairs)
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")

    dot.node('A', 'King Arthur')
    dot.node('B', 'Sir Bedevere the Wise')
    dot.node('L', 'Sir Lancelot the Brave')

    dot.edges(['AB', 'AL'])
    dot.edge('B', 'L', constraint='false')

    s = Source(dot.source, filename="ddg.gv", format="png")
    s.view()

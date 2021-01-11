from __future__ import print_function
import sys
import random

from graphviz import Digraph
from graphviz import Source

sys.path.extend(['.', '..'])

from pycparser import c_parser, c_ast

last_node = ""


def parse_list_inside_operation(dot, pairs, block_items):
    length = len(block_items)
    for j in range(length):
        next_op = block_items[j]
        # print(next_op)
        if isinstance(next_op, c_ast.Assignment):
            dot, pairs = add_to_graph_assignment(dot, pairs, next_op)
        elif isinstance(next_op, c_ast.Decl):
            dot, pairs = add_to_graph_decl(dot, pairs, next_op)
        elif isinstance(next_op, c_ast.Return):
            dot, pairs = add_to_graph_return(dot, pairs, next_op)
        elif isinstance(next_op, c_ast.If):
            dot, pairs = add_to_graph_if(dot, pairs, next_op)
        elif isinstance(next_op, c_ast.For):
            dot, pairs = add_to_graph_for(dot, pairs, next_op)

    return dot, pairs


def unary_op_to_str(unary_op):
    op = unary_op.op
    expr = unary_op.expr.name
    str = op.__str__() + expr.__str__()
    return str, expr


def binary_op_to_str(bin_op):
    op = bin_op.op
    left = bin_op.left
    right = bin_op.right
    if isinstance(left, c_ast.ID):
        left_str = left.name.__str__()
    if isinstance(left, c_ast.Constant):
        left_str = left.value.__str__()

    if isinstance(right, c_ast.ID):
        right_str = right.name.__str__()
    if isinstance(right, c_ast.Constant):
        right_str = right.value.__str__()

    op_string = left_str + " " + op.__str__() + " " + right_str
    # print(type(left), type(right))
    return op_string, left, right


def add_to_graph_assignment(dot, pairs, operation):
    # print(operation)
    op = operation.op
    left = operation.lvalue
    right = operation.rvalue
    if isinstance(left, c_ast.ID):
        left_str = left.name.__str__()

    if isinstance(right, c_ast.ID):
        right_str = right.name.__str__()
    if isinstance(right, c_ast.Constant):
        right_str = right.value.__str__()
    if isinstance(right, c_ast.BinaryOp):
        right_str, l, r = binary_op_to_str(right)

    op_string = left_str + " " + op.__str__() + " " + right_str
    before_name = pairs[left.name]
    new_name = before_name + "1"
    pairs[left.name] = new_name
    dot.node(new_name, op_string, shape='box')
    global last_node
    dot.edge(last_node, new_name, constraint='true', color="white")
    last_node = new_name
    # print(op_string)

    # стрелки
    if isinstance(right, c_ast.ID):
        dot.edge(pairs[right.name], new_name, constraint='true', color="black")
    if isinstance(right, c_ast.BinaryOp):
        dot.edge(pairs[r.name], new_name, constraint='true', color="black")
        dot.edge(pairs[l.name], new_name, constraint='true', color="black")
        # print("BinaryOp", l.name, r.name)

    return dot, pairs


def add_to_graph_decl(dot, pairs, operation):
    str_to_dot = ""
    name_val = operation.name
    init_value = operation.init
    if init_value is None:
        str_to_dot = name_val + " = ?"
    else:
        str_to_dot = name_val + " = " + init_value.value

    pairs[name_val] = name_val + "1"
    dot.node(pairs[name_val], str_to_dot, shape='box')
    global last_node
    dot.edge(last_node, pairs[name_val], constraint='true', color="white")
    last_node = pairs[name_val]

    return dot, pairs


def add_to_graph_return(dot, pairs, operation):
    return_var = operation.expr.name
    str_to_dot = "return " + return_var
    r = random.randint(1, 100)
    blok_name = "return" + r.__str__()
    # print(blok_name)
    dot.node(blok_name, str_to_dot, shape='box')

    # что за вохвращаемое значение
    dot.edge(pairs[return_var], blok_name, constraint='false', color="black")
    return dot, pairs


def add_to_graph_if(dot, pairs, operation):
    op_string, l, r = binary_op_to_str(operation.cond)
    # op_string = op_left.name.__str__() + oper.__str__() + op_right.value.__str__()
    global last_node
    dot.node(op_string, op_string, shape='diamond')
    dot.edge(last_node, op_string, constraint='true', color="white")
    dot.edge(pairs[l.name], op_string, constraint='true', color="black")
    last_node = op_string

    # print("___________________________________________")
    list_true = operation.iftrue
    if list_true is not None:
        items = list_true.block_items
        dot, pairs = parse_list_inside_operation(dot, pairs, items)

    # print("___________________________________________")
    list_false = operation.iffalse
    if list_false is not None:
        items = list_true.block_items
        dot, pairs = parse_list_inside_operation(dot, pairs, items)
    # print(operation.iffalse)
    return dot, pairs


def add_to_graph_for(dot, pairs, operation):
    # print(operation)
    for_init = operation.init.decls
    length = len(for_init)
    for j in range(length):
        next_op = for_init[j]
        dot, pairs = add_to_graph_decl(dot, pairs, next_op)

    for_cond = operation.cond
    cond_string, l, r = binary_op_to_str(for_cond)
    global last_node
    dot.node(cond_string, cond_string, shape='diamond')
    dot.edge(last_node, cond_string, constraint='true', color="white")
    last_node = cond_string

    for_stmt = operation.stmt
    if for_stmt is not None:
        items = for_stmt.block_items
        dot, pairs = parse_list_inside_operation(dot, pairs, items)
    # print(for_stmt)

    for_next = operation.next
    str, val = unary_op_to_str(for_next)
    before_val = pairs[val]
    new_val = before_val + "1"
    pairs[val] = new_val
    # print(str, pairs[val])
    dot.node(new_val, str, shape='box')
    # расположние
    dot.edge(last_node, new_val, constraint='true', color="white")
    last_node = new_val
    # стрелки
    dot.edge(before_val, new_val, constraint='true', color="black")
    dot.edge(new_val, new_val, constraint='true', color="black")
    dot.edge(new_val, cond_string, constraint='true', color="black")
    return dot, pairs


def comand_list_parser(operations, dots, pairss):
    length = len(operations)
    # print(operations)
    # print(length)
    for j in range(length):
        # print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
        next_op = operations[j][1]
        # print(j, type(next_op))
        if isinstance(next_op, c_ast.Assignment):
            dots, pairss = add_to_graph_assignment(dots, pairss, next_op)
        elif isinstance(next_op, c_ast.Decl):
            dots, pairss = add_to_graph_decl(dots, pairss, next_op)
        elif isinstance(next_op, c_ast.Return):
            dots, pairss = add_to_graph_return(dots, pairss, next_op)
        elif isinstance(next_op, c_ast.If):
            dots, pairss = add_to_graph_if(dots, pairss, next_op)
        elif isinstance(next_op, c_ast.For):
            dots, pairss = add_to_graph_for(dots, pairss, next_op)
        # print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
    return dots, pairss


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
    last_node = 'fun_decl'
    compound = nodes.children()[1][1]
    operations = compound.children()
    dot, pairs = comand_list_parser(operations, dot, pairs)

    s = Source(dot.source, filename="ddg.gv", format="png")
    s.view()

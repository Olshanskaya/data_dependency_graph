#-----------------------------------------------------------------
# pycparser: explore_ast.py
#
# This example demonstrates how to "explore" the AST created by
# pycparser to understand its structure. The AST is a n-nary tree
# of nodes, each node having several children, each with a name.
# Just read the code, and let the comments guide you. The lines
# beginning with #~ can be uncommented to print out useful
# information from the AST.
# It helps to have the pycparser/_c_ast.cfg file in front of you.
#
# Eli Bendersky [https://eli.thegreenplace.net/]
# License: BSD
#-----------------------------------------------------------------
from __future__ import print_function
import sys

# This is not required if you've installed pycparser into
# your site-packages/ with setup.py
#
sys.path.extend(['.', '..'])

from pycparser import c_parser, c_ast

# This is some C source to parse. Note that pycparser must begin
# at the top level of the C file, i.e. with either declarations
# or function definitions (this is called "external declarations"
# in C grammar lingo)
#
# Also, a C parser must have all the types declared in order to
# build the correct AST. It doesn't matter what they're declared
# to, so I've inserted the dummy typedef in the code to let the
# parser know Hash and Node are types. You don't need to do it
# when parsing real, correct C code.

text = """
int fibonacci_naive(int n) {
    if (n <= 1)
        return n;
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2);
}

"""

# Create the parser and ask to parse the text. parse() will throw
# a ParseError if there's an error in the code
#
parser = c_parser.CParser()
ast = parser.parse(text, filename='<none>')

# Uncomment the following line to see the AST in a nice, human
# readable way. show() is the most useful tool in exploring ASTs
# created by pycparser. See the c_ast.py file for the options you
# can pass it.
ast.show(showcoord=True)



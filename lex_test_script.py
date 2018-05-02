from py_lex_test import MyLexer
from py_parser_test import MyParser
import sys


lexer = MyLexer()
parser = MyParser()

line = '0'

while line:
    try:
        print parser.parse(lexer.get_token_list(line))
        line = raw_input('>>  ')
    except:
        print 'Dumping all values:'
        for ident, value in parser.variables.iteritems():
            print ident, '=', value
        exit(0)




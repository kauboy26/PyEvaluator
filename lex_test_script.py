from py_lex_test import MyLexer
from py_parser_test import MyParser
import sys


lexer = MyLexer()
parser = MyParser()

line = '0'
print 'Type "help" for more info.\n'

while line:
    print parser.parse(lexer.get_token_list(line))
    line = raw_input('>>  ')
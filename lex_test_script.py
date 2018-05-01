from py_lex_test import MyLexer
from py_parser_test import MyParser

in_str = '18 + 8 * 9 - (1 - 1) - 9 * 3'

lexer = MyLexer(in_str)

parser = MyParser()

print 'Result:', parser.parse(lexer.get_token_list())
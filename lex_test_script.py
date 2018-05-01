from py_lex_test import MyLexer
from py_parser_test import MyParser

in_str = '8 + 8 * (8)'

lexer = MyLexer(in_str)
parser = MyParser()

print 'Result:', parser.parse(lexer.get_token_list())
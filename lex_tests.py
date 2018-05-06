import py_lex_test
import py_parser_test

print 'Begin by testing the lexer\'s helper methods'
assert(py_lex_test.is_numeric('9'))
assert(py_lex_test.is_numeric('0'))
assert(not py_lex_test.is_numeric('a'))

assert(py_lex_test.is_alpha('a'))
assert(py_lex_test.is_alpha('z'))
assert(py_lex_test.is_alpha('A'))
assert(py_lex_test.is_alpha('Z'))
assert(not py_lex_test.is_alpha('['))

assert(py_lex_test.is_alphanumeric('a'))
assert(py_lex_test.is_alphanumeric('z'))
assert(py_lex_test.is_alphanumeric('A'))
assert(py_lex_test.is_alphanumeric('Z'))
assert(py_lex_test.is_alphanumeric('0'))
assert(py_lex_test.is_alphanumeric('9'))
assert(not py_lex_test.is_alphanumeric('['))

assert(py_lex_test.is_special('(')) # I'm not going to bother with the rest



lexer = py_lex_test.MyLexer()

assert(lexer.get_token_list('') == [('EOL', None)])
assert(lexer.get_token_list('9 + 90 * (- as8df') == [('NUM', 9), ('+', None), ('NUM', 90), ('*', None), ('(', None),
    ('-', None), ('ID', 'as8df'), ('EOL', None)])
assert(lexer.get_token_list('2 4 56') == [('NUM', 2), ('NUM', 4), ('NUM', 56), ('EOL', None)])

assert(lexer.get_token_list('212.312 4.33 00.000') == [('NUM', 212.312), ('NUM', 4.33), ('NUM', 0), ('EOL', None)])
assert(lexer.get_token_list('2.') == [('NUM', 2), ('EOL', None)])
assert(lexer.get_token_list('1.1.2') == [('NUM', 1.1), ('NUM', 2), ('EOL', None)])


print '\nParser stuff\n'
parser = py_parser_test.MyParser()

assert(parser.parse(lexer.get_token_list('9 + 9')) == 18.0)
assert(parser.parse(lexer.get_token_list('9 * (1 - 3)')) == -18.0)
assert(parser.parse(lexer.get_token_list('2 * 5 * (7 * 3) - 15')) == 195.0)
assert(parser.parse(lexer.get_token_list('a = 9')) == 9.0)
assert(parser.parse(lexer.get_token_list('a = b')) == None)
assert(parser.parse(lexer.get_token_list('a')) == 9.0)
assert(parser.parse(lexer.get_token_list('a = a + 7')) == 16.0)
assert(parser.parse(lexer.get_token_list('5 + a * 2')) == 37)
assert(parser.parse(lexer.get_token_list('pow(a + 4, 2)')) == 400)
assert(parser.parse(lexer.get_token_list('pow(pow(pow(pow(a - 18, 2), 2), 2), 2)')) == 256 ** 2)
assert(parser.parse(lexer.get_token_list('9 ++ 9')) == None)
assert(parser.parse(lexer.get_token_list('34 - c')) == None)
assert(parser.parse(lexer.get_token_list('c = ')) == None)
assert(parser.parse(lexer.get_token_list('b = 18 + pow(5)')) == None)
assert(parser.parse(lexer.get_token_list('b = 1 - 4 - 5 - 1')) == -9)
assert(parser.parse(lexer.get_token_list('89 = b')) == None)

print '\nfunction defintion stuff\n'
assert(parser.parse(lexer.get_token_list('def f(a, b, c) = a * b + c')) == None)
assert(parser.parse(lexer.get_token_list('f(2, 3, 4)')) == 10)
assert(parser.parse(lexer.get_token_list('def g(a) = f(a - 1, a - 2, a - 3)')) == None)
assert(parser.parse(lexer.get_token_list('a = g(8)')) == 47)
assert(parser.parse(lexer.get_token_list('def hello(param) = g(param) * g(param) * pow(g(param), 1)')) == None)
assert(parser.parse(lexer.get_token_list('world = 4')) == 4)
assert(parser.parse(lexer.get_token_list('hello(world)')) == 343)
assert(parser.parse(lexer.get_token_list('def truck(one, two, three) = 1 * one + 2 * two + 3 * three')) == None)
assert(parser.parse(lexer.get_token_list('truck(4, 5, 6)')) == 32)

print '\nbroken func definitions\n'
assert(parser.parse(lexer.get_token_list('bad = 20')) == 20)
assert(parser.parse(lexer.get_token_list('def bad(e) = e')) == None)
assert(parser.parse(lexer.get_token_list('bad(10)')) == None)

print '\nbreak params\n'
assert(parser.parse(lexer.get_token_list('def bruck(a, e, 3) = a + e + 3')) == None)
assert(parser.parse(lexer.get_token_list('bruck(1, 1, 1)')) == None)

print '\nEmpty params\n'
assert(parser.parse(lexer.get_token_list('def goodboy() = 2')) == None)
assert(parser.parse(lexer.get_token_list('goodboy()')) == 2)
assert(parser.parse(lexer.get_token_list('goodboy(8)')) == None)
assert(parser.parse(lexer.get_token_list('def superpow(a, b) = pow(pow(a, b), pow(a, b))')) == None)
assert(parser.parse(lexer.get_token_list('yes = superpow(2, 2)')) == 256)
assert(parser.parse(lexer.get_token_list('superpow = 2')) == None)
assert(parser.parse(lexer.get_token_list('def badd() = 2')) == None)
assert(parser.parse(lexer.get_token_list('badd() * badd()')) == 4)
assert(parser.parse(lexer.get_token_list('17 * badd()')) == 34)
assert(parser.parse(lexer.get_token_list('def this(a, b) = a - b')) == None)
assert(parser.parse(lexer.get_token_list('this(1 3)')) == None)
assert(parser.parse(lexer.get_token_list('this(1,)')) == None)
assert(parser.parse(lexer.get_token_list('this(1 3,)')) == -2)  # Hahaha this thing works! Need to fix this later

print '\nMore nested function calls\n'
assert(parser.parse(lexer.get_token_list('def gg(a, b, c) = goodboy() * badd() /4 * a')) == None)
assert(parser.parse(lexer.get_token_list('gg(pow(3, 2), 8, pow(pow(1, 2), 5))')) == 9)

print '\n......................'
print 'All tests passed!'
import sys

"""
The lexer and parser here are much much much simpler than the thing
found in the PyEvaluator project. Just figuring some shit out here
with regards to code generation.
"""

def get_token_list(in_str='0'):
    """
    Support only nums (no floats), (), +, *
    """
    length = len(in_str)
    tk_list = []
    
    i = 0
    while i < length:
        if in_str[i] >= '0' and in_str[i] <= '9':
            # FOund a number, grab it
            num = 0
            while i < length and in_str[i] >= '0' and in_str[i] <= '9':
                num = num * 10 + int(in_str[i])
                i = i + 1

            tk_list.append(('N', num))

        elif in_str[i] == '(' or in_str[i] == ')' or in_str[i] == '+' or in_str[i] == '*':
            tk_list.append((in_str[i], None))
            i = i + 1

        else:
            # eat it up
            i = i + 1

    return tk_list

def set(reg, number):
    # For now assume it's less than 15.
    # I realize this is an efficient way of doing this, when I can double
    # the number by adding it to itself. However, I'm just letting this be for now
    print 'AND', reg, ',', reg, ',', 0, '; set', reg, 'to', number
    if number == 0:
        return

    if (number > 15):
        for i in xrange(number / 15):
            print 'ADD', reg, ',', reg, ', 15'
        if number % 15:
            print 'ADD', reg, ',', reg, ',', number % 15
    elif (number < -16):
        for i in xrange(- number / 16):
            print 'ADD', reg, ',', reg, ', -16'
        if number % 16:
            print 'ADD', reg, ',', reg, ',', (number % 16) - 16
    else:
        print 'ADD', reg, ',', reg, ',', number


def push_result(reg, sp):
    # pushes val to the stack, where SP is stack pointer
    print 'ADD', sp, ',', sp, ', -1', '; push value in', reg, 'to stack'
    print 'STR', reg, ',', sp, ',', 0

def pop_into(reg, sp):
    # pops the thing on top of the stack into specified registre,
    # where SP is stack pointer
    print 'LDR', reg, ',', sp, ',', 0, '; pop into', reg
    print 'ADD', sp, ',', sp, ', 1' 

def add(sr1_and_dst, sr2):
    print 'ADD', sr1_and_dst, ',', sr1_and_dst, ',', sr2, '; ADD'

def mult():
    print 'JSR MULT'


def parse(in_str='0'):
    print '; The result will be in R0'

    tk_list = get_token_list(in_str)
    tk_list.append(('END', None))

    precendence = {'+': 10, '*': 20, '(': 0, ')': 1, 'END': -1000}

    num_stack = []
    op_stack = []

    length = len(tk_list)
    i = 0
    while (i < length):
        typ, val = tk_list[i]

        if typ == 'N':
            num_stack.append(('N', val))
            i = i + 1
        else:

            if typ == '(':
                op_stack.append('(')
                i = i + 1
                continue

            # hit operand
            while op_stack and precendence[typ] <= precendence[op_stack[-1]]:
                # pop two values from num stack and do whatever
                op = op_stack.pop()
                n, val1 = num_stack.pop()
                if n == 'N':
                    set('R0', val1)
                elif n == '$':
                    pop_into('R0', 'R6')


                n, val2 = num_stack.pop()
                if n == 'N':
                    set('R1', val2)
                elif n == '$':
                    pop_into('R1', 'R6')

                if (op == '+'):
                    add('R0', 'R1')
                elif (op == '*'):
                    mult()
                else:
                    print 'SHTI'

                num_stack.append(('$', None))
                push_result('R0', 'R6')

            if typ == ')':
                # Expect a '('
                op_stack.pop()
            else:
                op_stack.append(typ)

            i = i + 1

    if num_stack:
        n, val = num_stack.pop()
        if n == 'N':
            set('R0', val)
        elif n == '$':
            pop_into('R0', 'R6')

def print_mult():
    s =\
    """
    ; Take in args in r0 and r1, non neg nums only
    MULT       AND R2, R2, 0       ; use R3 to accumlate the result
        
                ADD R1, R1, 0
    MLOOP      BRnz MULT_RET
                ADD R2, R2, R0
                ADD R1, R1, -1
                BR MLOOP

    MULT_RET    ADD R0, R2, 0

                RET
    """
    print s

if __name__ == '__main__':
    if len(sys.argv) == 1: # or len(sys.argv) > 2:
        print 'Usage:\n', 'python lp.py <your expression within double quotes>'

    else:
        print '; Attempting to convert "', sys.argv[-1], '"'

        print '.orig x3000'
        print 'LD R6, STACK\n'
        parse(sys.argv[-1])
        print 'HALT'
        print 'STACK .fill xF000'
        
        print_mult()
        print '.end'
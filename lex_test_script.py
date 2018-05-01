from py_lex_test import MyLexer

def perform_operation(val1, val2, operation):
    if operation == '*':
        return val1 * val2
    elif operation == '+':
        return val1 + val2
    elif operation == '/':
        return val1 / val2
    elif operation == '-':
        return val1 - val2

    print 'Bad operand!'
    exit(1)

lex = MyLexer('(9 - (3 + 1)) * 2 - 2 / 1')

tk_list = lex.get_token_list()

op_stack = []
num_stack = []

precedence = {'*': 5, '/': 5, '+': 4, '-': 4, 'EOF': 0, '(': 0, ')':0}

i =0
while i < len(tk_list):

    tk_type, value = tk_list[i]

    if tk_type == 'NUM':
        num_stack.append(value)
    else:
        if tk_type == '(':
            op_stack.append(tk_type)
            i = i + 1
            continue

        if tk_type == ')':
            while op_stack and op_stack[-1] != '(':
                val2 = num_stack.pop()
                val1 = num_stack.pop()
                operation = op_stack.pop()
                new_val = perform_operation(val1, val2, operation)
                num_stack.append(new_val)

            if not op_stack:
                print 'Mismatched parens.'
                exit(2)
            else:
                op_stack.pop()
                i = i + 1
                continue

        while op_stack and precedence[tk_type] <= precedence[op_stack[-1]]:
            # When Ilooking at the current operand token,
            # if it has a lower precedence then the topmost thing
            # on the operand stack, keep popping off the num and op stacks
            # and evaluate and push
            val2 = num_stack.pop()
            val1 = num_stack.pop()
            operation = op_stack.pop()

            new_val = perform_operation(val1, val2, operation)

            num_stack.append(new_val)

        # At this point, either the operand stack is empty, or the top most
        # operand has a precedence lower than the newest operand
        op_stack.append(tk_type)
    i = i + 1

print 'Result:', num_stack.pop()
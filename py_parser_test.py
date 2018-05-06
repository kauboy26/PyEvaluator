import math

FAILURE = 0
SUCCESS = 1

class MyParser():
    def __init__(self):
        # will store the values of variables
        self.variables = {}
        self.precedence =\
            {'*': 50, '/': 50, '%':50, '+': 40, '-': 40,
            'sin': 60, 'sqrt': 60, 'pow': 60,   # include special functions like these
            '(': 0, ')':1, ',': 5, '=': 10,
            'EOL':0}

        # denotes the number of arguments needed when that function is performed.
        self.args_needed =\
            {'*': 2, '/': 2, '%':2, '+': 2, '-': 2, '=': 2,
            'sin':1, 'sqrt': 1, 'pow':2}

        self.functions = {'sin':0, 'sqrt':0, 'pow':0}

    def perform_operation(self, operands, operation):
        # The operands MUST be passed in reverse order!
        # eg. operands = [1, 2], operation = '-' will perform 2 - 1

        if operation == '*':
            result = operands[1] * operands[0]
        elif operation == '+':
            result = operands[1] + operands[0]
        elif operation == '/':
            if operands[0] == 0:
                print 'Cannot divide by 0.'
                return FAILURE, None
            result = operands[1] / operands[0]
        elif operation == '-':
            result = operands[1] - operands[0]
        elif operation == '%':
            if operands[0] == 0:
                print 'Cannot modulo by 0.'
                return FAILURE, None
            result = operands[1] % operands[0]
        elif operation == 'pow':
            result = operands[1] ** operands[0]
        elif operation == 'sin':
            result = math.sin(operands[0])

        return SUCCESS, result

    def parse(self, tk_list=[('EOL', None)]):
        op_stack = []
        num_stack = []

        # Use this to figure out whether not enough operands have been
        # pushed for the function to work.
        args_count_stack = [] 

        precedence = self.precedence

        i =0
        while i < len(tk_list):
            tk_type, value = tk_list[i]
            if tk_type == 'NUM':
                num_stack.append(value) # TODO Shall I convert this to a float?
            else:
                if tk_type == 'ID':
                    if value in self.functions:
                        tk_type = value
                    else:
                        # found a variable, go to next iteration.
                        num_stack.append(value)
                        i = i + 1
                        continue

                if tk_type == '(':
                    op_stack.append(tk_type)
                    i = i + 1
                    continue

                while op_stack and precedence[tk_type] <= precedence[op_stack[-1]]:
                    # When I am looking at the current operand token,
                    # if it has a lower precedence then the topmost thing
                    # on the operand stack, keep popping off the num and op stacks
                    # and evaluate and push
                    operation = op_stack.pop()
                    if len(num_stack) < self.args_needed[operation]:
                        print 'Not enough arguments to the function:', operation, '\nNeeded',\
                            self.args_needed[operation], 'but found', len(num_stack)
                        return None

                    if operation in self.functions:
                        if args_count_stack[-1] == self.args_needed[operation]:
                            args_count_stack.pop()
                        else:
                            print 'Incorrect number of arguments to the function:', operation, '\nNeeded',\
                                self.args_needed[operation], 'but found', args_count_stack[-1]
                            return None

                    # See note 1 from notes.md, for why '=' is being tested
                    # here an not in perform_operation
                    if operation == '=':
                        val2 = num_stack.pop()
                        val1 = num_stack.pop()
                        if type(val1) == str:
                            if type(val2) == str:
                                if val2 in self.variables:
                                    self.variables[val1] = self.variables[val2]
                                    return self.variables[val2]
                                else:
                                    print 'The variable', val2, 'has not been defined.'
                                    return None
                            else:
                                self.variables[val1] = val2
                                return val2
                        else:
                            print 'Cannot assign a value to a non-variable.'
                            return None

                    # Now for other operations, pass in a list of operand values
                    operands = []
                    for j in xrange(self.args_needed[operation]):
                        oper = num_stack.pop()
                        if type(oper) == str:
                            if oper in self.variables:
                                # The operands are being passed in reverse order
                                operands.append(self.variables[oper])
                            else:
                                print 'The variable', oper, 'has not been defined.'
                                return None
                        else:
                            operands.append(oper)
                    
                    was_success, new_val = self.perform_operation(operands, operation)

                    if not was_success:
                        return None
                    num_stack.append(new_val)

                # At this point, either the operand stack is empty, or the top most
                # operand has a precedence lower than the newest operand.
                if tk_type == ')':
                    # The thing we stopped on must be '(', otherwise mismatch
                    if not op_stack or op_stack[-1] != '(':
                        print 'Mismatched parens.'
                        return None
                    op_stack.pop()

                elif tk_type == ',':
                    if not args_count_stack:
                        print '"," must appear to separate function arguments.'
                        return None
                    else:
                        args_count_stack[-1] = args_count_stack[-1] + 1
                    # We don't push ',' on to the stack.
                else:
                    if tk_type in self.functions:
                        args_count_stack.append(1)
                    op_stack.append(tk_type)

            i = i + 1

        if num_stack:
            if len(num_stack) > 1:
                print 'Not enough operators?'
                return None
            else:
                result = num_stack.pop()
                if type(result) == str:
                    if result in self.variables:
                        return self.variables[result]
                    else:
                        print 'The variable', result, 'has not been defined.'
                        return None
                else:
                    return result
        else:
            print 'Faulty expression!'
            return None

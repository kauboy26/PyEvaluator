FAILURE = 0
SUCCESS = 1

class MyParser():
    def __init__(self):
        # will store the values of variables
        self.variables = {}
        self.precedence =\
            {'*': 50, '/': 50, '%':50, '+': 40, '-': 40,
            'sin': 60, 'sqrt': 60, 'pow': 60,   # include special functions like these
            '(': 0, ')':0, '=': 10,
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

        return SUCCESS, result

    def parse(self, tk_list=[('EOL', None)]):
        op_stack = []
        num_stack = []
        precedence = self.precedence

        i =0
        while i < len(tk_list):
            tk_type, value = tk_list[i]
            if tk_type == 'NUM':
                num_stack.append(value) # TODO Shall I convert this to a float?
            elif tk_type == 'ID':
                # The token may be a function, so make sure it isn't
                num_stack.append(value)
            else:
                if tk_type == '(':
                    op_stack.append(tk_type)
                    i = i + 1
                    continue

                if tk_type == ')':
                    while op_stack and op_stack[-1] != '(':
                        operation = op_stack.pop()
                        if len(num_stack) < self.args_needed[operation]:
                            print 'Not enough arguments!'
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

                    if not op_stack:
                        print 'Mismatched parens.'
                        return None
                    else:
                        op_stack.pop()
                        i = i + 1
                        continue

                while op_stack and precedence[tk_type] <= precedence[op_stack[-1]]:
                    # When Ilooking at the current operand token,
                    # if it has a lower precedence then the topmost thing
                    # on the operand stack, keep popping off the num and op stacks
                    # and evaluate and push
                    operation = op_stack.pop()
                    if len(num_stack) < self.args_needed[operation]:
                        print 'Not enough arguments!'
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
                # operand has a precedence lower than the newest operand
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

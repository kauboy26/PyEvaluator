FAILURE = 0
SUCCESS = 1

class MyParser():
    def __init__(self):
        # will store the values of variables
        self.variables = {}
        self.precedence = {'*': 5, '/': 5, '%':5, '+': 4, '-': 4, 'EOL': 0, '(': 0, ')':0, '=': 1} 

    def perform_operation(self, val1, val2, operation):
        # Depending on what val1 and val2 are (ints or strings?),
        # this method does whatever and checks the validity of that
        # expression. However, I don't know if checking their types
        # is the most elegant or efficient way of going about this.
        val1_is_str = type(val1) == str
        val2_is_str = type(val2) == str

        if operation == '=':
            if not val1_is_str:
                print 'Cannot assign value to a number'
                return FAILURE, None
            else:
                if not val2_is_str:
                    self.variables[val1] = val2
                    return SUCCESS, val2
                else:
                    if val2 not in self.variables:
                        print 'The variable', val2, 'has not been defined.'
                        return FAILURE, None
                    else:
                        self.variables[val1] = self.variables[val2]
                        return SUCCESS, self.variables[val2]

        # Since the '=' operator is the only operator in which one of the variables (the left hand one)
        # is allowed to not exist, from this point onwards, all the operations will require both to exist
        if val1_is_str:
            if val1 not in self.variables:
                print 'The variable', val1, 'has not been defined'
                return FAILURE, None
            else:
                value1 = self.variables[val1]
        else:
            value1 = val1

        if val2_is_str:
            if val2 not in self.variables:
                print 'The variable', val2, 'has not been defined'
                return FAILURE, None
            else:
                value2 = self.variables[val2]
        else:
            value2 = val2

        result = 0

        if operation == '*':
            result = value1 * value2
        elif operation == '+':
            result = value1 + value2
        elif operation == '/':
            result = value1 / value2
        elif operation == '-':
            result = value1 - value2
        elif operation == '%':
            result = value1 % value2

        return SUCCESS, result

    def parse(self, tk_list=[('EOL', None)]):
        op_stack = []
        num_stack = []
        precedence = self.precedence

        i =0
        while i < len(tk_list):
            tk_type, value = tk_list[i]
            if tk_type == 'NUM' or tk_type == 'ID':
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
                        was_success, new_val = self.perform_operation(val1, val2, operation)
                        if not was_success:
                            # Happens when operators had a bust
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
                    val2 = num_stack.pop()
                    val1 = num_stack.pop()
                    operation = op_stack.pop()
                    was_success, new_val = self.perform_operation(val1, val2, operation)
                    if not was_success:
                        # Happens when operators had a bust
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

class MyParser():
    def __init__(self):
        # will store the values of variables
        self.variables = {}
        self.precedence = {'*': 5, '/': 5, '+': 4, '-': 4, 'EOL': 0, '(': 0, ')':0, '=': 1} 

    def perform_operation(self, val1, val2, operation):
        # Depending on what val1 and val2 are (ints or strings?),
        # this method does whatever and checks the validity of that
        # expression. However, I don't know if checking their types
        # is the most elegant or efficient way of going about this.
        val1_is_str = type(val1) == str
        val2_is_str = type(val2) == str

        if val1_is_str:
            if val1 in self.variables:
                value1 = self.variables[val1]
            else:
                self.variables[val1] = 0
                value1 = 0
        else:
            value1 = val1

        if val2_is_str:
            if val2 in self.variables:
                value2 = self.variables[val2]
            else:
                self.variables[val2] = 0
                value2 = 0
        else:
            value2 = val2

        if operation == '=':
            if not val1_is_str:
                print 'Cannot assign value to a number'
                return 999
            else:
                self.variables[val1] = value2
                return value2

        if operation == '*':
            return value1 * value2
        elif operation == '+':
            return value1 + value2
        elif operation == '/':
            return value1 / value2
        elif operation == '-':
            return value1 - value2

        print 'Bad operand!'
        return 999

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
                        new_val = self.perform_operation(val1, val2, operation)
                        num_stack.append(new_val)

                    if not op_stack:
                        print 'Mismatched parens.'
                        return 999
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
                    new_val = self.perform_operation(val1, val2, operation)
                    num_stack.append(new_val)

                # At this point, either the operand stack is empty, or the top most
                # operand has a precedence lower than the newest operand
                op_stack.append(tk_type)
            i = i + 1

        if num_stack:
            if len(num_stack) > 1:
                print 'Not enough operators?'
                return 999
            else:
                result = num_stack.pop()
                if type(result) == str:
                    if result in self.variables:
                        return self.variables[result]
                    else:
                        print 'Has this variable been defined? :', result 
                        return 999
                else:
                    return result
        else:
            print 'Faulty expression!'
            return 999

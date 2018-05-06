import math

FAILURE = 0
SUCCESS = 1

HIGHEST_PREC = 60

class MyParser():
    def __init__(self):
        # will store the values of variables
        self.variables = {}
        self.precedence =\
            {'*': 50, '/': 50, '%':50, '+': 40, '-': 40,
            'sin': HIGHEST_PREC, 'sqrt': HIGHEST_PREC, 'pow': HIGHEST_PREC,   # include special functions like these
            '(': 0, ')':1, ',': 5, '=': 10,
            'EOL':0}

        # denotes the number of arguments needed when that function is performed.
        self.args_needed =\
            {'*': 2, '/': 2, '%':2, '+': 2, '-': 2, '=': 2,
            'sin':1, 'sqrt': 1, 'pow':2}

        self.functions = {'sin':0, 'sqrt':0, 'pow':0}

        self.user_functions = {}

    def perform_operation(self, operands, operation):
        # The operands MUST be passed in reverse order!
        # eg. operands = [1, 2], operation = '-' will perform 2 - 1
        if operation not in self.user_functions:
            return self.perform_primitive_operation(operands, operation)

        # If it's a user defined function:
        func_def = self.user_functions[operation]
        num_stack = []

        operand_stack = []

        if len(func_def) == 1:
            typ, val = func_def[0]
            if typ == 'C':
                return SUCCESS, val
            elif typ == 'A':
                return SUCCESS, operands[val]


        operands.reverse()

        for typ, val in func_def:
            if typ == 'C':
                if val == '$':
                    operand_stack.append(num_stack.pop())
                else:
                    operand_stack.append(val)
            elif typ == 'A':
                operand_stack.append(operands[val])
            elif typ == 'O':
                status, result = self.perform_operation(operand_stack, val)
                if status == FAILURE:
                    return FAILURE, None
                operand_stack = []
                num_stack.append(result)

        return SUCCESS, num_stack.pop()

    def perform_primitive_operation(self, operands, operation):
        # The operands must be in reverse order.

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
        if len(tk_list) > 0:
            if tk_list[0][1] == 'help':
                print 'Type in any expressions or assignment statements you want.'
                print 'For example:'
                print '>>  a = 1 + 1'
                print '2'
                print '>>  a = a + 3'
                print '5'
                print 'Type "print" to see all values and defined functions.\n'
                return None
            if tk_list[0][1] == 'print':
                print 'Printing variables:'
                for key, value in self.variables.iteritems():
                    print key, '=', value
                print '\nDefined functions:'
                for key, value in self.args_needed.iteritems():
                    print 'The function', key, 'requires', value, 'arguments'
                return None
            if tk_list[0][1] == 'def':
                was_success = self.parse_definition(tk_list)
                if was_success:
                    print 'Function defined.'
                return None

        op_stack = []
        num_stack = []

        # Use this to figure out whether not enough operands have been
        # pushed for the function to work.
        args_count_stack = [] 

        precedence = self.precedence

        i = 0
        while i < len(tk_list):
            tk_type, value = tk_list[i]
            if tk_type == 'NUM':
                num_stack.append(value)
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

    def parse_definition(self, tk_list=[('EOL', None)]):
        """
        This method is used to parse function definitions. The function must be
        defined in the form:
        def f(x, y, z, ..) = x * 8 * (z + 3)
        All functions that are called within this function must already be defined;
        therefore, it is NOT possible to define a recursive function.

        Since the function definition follows this rigid structure, I will be taking some shortcuts.
        """

        i = 0 # I will use this to manually traverse the token list

        # def
        if tk_list[i][1] != 'def':
            print 'Malformed function definition.'
            return FAILURE
        i = i + 1

        func_name = tk_list[i][1]
        if func_name in self.variables:
            print 'Function name is already taken by a variable.'
            return FAILURE
        i = i + 1

        if tk_list[i][0] != '(':
            print 'Missing "(", malformed function definition.'
            return FAILURE
        i = i + 1

        # The early filler is parsed, go collect arguments
        arg_index = 0
        num_args = 0
        args = {}
        while i < len(tk_list) and tk_list[i][0] != ')':
            token, value = tk_list[i]
            if token != 'ID':
                if token == ',':
                    arg_index = arg_index + 1
                else:
                    print 'Malformed formal parameters in function defintion.'
                    return FAILURE
            else:
                args[value] = arg_index
                num_args = num_args + 1
            i = i + 1

        # At this point, either should have hit a ')' or screwed up something
        if tk_list[i][0] != ')':
            print 'Mismatched parens in function definition.'
            return FAILURE

        if arg_index != num_args - 1:
            print 'Incorrect number of commas separating formal params.'
            return FAILURE

        # Skip the ')'
        i = i + 1

        if tk_list[i][0] != '=':
            print 'Malformed function definition, misplaced "="'
            return FAILURE
        i = i + 1

        # Now finally, for the task of parsing the definition of the function
        pseudo_num_stack = []
        op_stack = []
        def_stack = [] # will hold the polish notation
        args_count_stack = [] # NOT to confuse with formal arguments, this structure is
                                # used to keep track of functions appearing within
        precedence = self.precedence

        while i < len(tk_list):
            tk_type, value = tk_list[i]
            if tk_type == 'NUM':
                pseudo_num_stack.append(('C', value)) # a constant
            else:
                if tk_type == 'ID':
                    if value in self.functions:
                        tk_type = value
                    else:
                        pseudo_num_stack.append(('A', value)) # argument
                        i = i + 1
                        continue

                if tk_type == '(':
                    op_stack.append(tk_type)
                    i = i + 1
                    continue

                while op_stack and precedence[tk_type] <= precedence[op_stack[-1]]:
                    operation = op_stack.pop()
                    if len(pseudo_num_stack) < self.args_needed[operation]:
                        print 'Not enough arguments to the function:', operation, '\nNeeded',\
                            self.args_needed[operation], 'but found', len(pseudo_num_stack)
                        return FAILURE

                    if operation in self.functions:
                        if args_count_stack[-1] == self.args_needed[operation]:
                            args_count_stack.pop()
                        else:
                            print 'Incorrect number of arguments to the function:', operation, '\nNeeded',\
                                self.args_needed[operation], 'but found', args_count_stack[-1]
                            return FAILURE

                    if operation == '=':
                        print "Cannot assign values within functions."
                        return FAILURE

                    # Pop the required amount off the stack
                    for j in xrange(self.args_needed[operation]):
                        typ, val = pseudo_num_stack.pop()
                        if typ == 'C':
                            def_stack.append((typ, val))
                        elif typ == 'A':
                            if val in args:
                                def_stack.append((typ, args[val]))
                            else:
                                print 'Variable not in formal params!'
                                return FAILURE

                    def_stack.append(('O', operation))
                    pseudo_num_stack.append(('C', '$'))
                # END WHILE

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

        if pseudo_num_stack:
            if len(pseudo_num_stack) > 1:
                print 'Not enough operators?'
                return FAILURE
            else:
                self.functions[func_name] = 0
                self.precedence[func_name] = HIGHEST_PREC
                self.args_needed[func_name] = num_args
                if not def_stack:
                    typ, val = pseudo_num_stack.pop()
                    if typ == 'C':
                        def_stack.append(('C', val))
                    else:
                        def_stack.append(('A', args[val]))
                self.user_functions[func_name] = def_stack
        else:
            print 'Faulty expression in function definition!'
            return FAILURE      

        return SUCCESS
import math

import miscell

FAILURE = 0
SUCCESS = 1

HIGHEST_PREC = 60

class MyParser():
    def __init__(self):
        # will store the values of variables
        self.variables = {'pi': math.pi, 'e': math.e}
        self.precedence =\
            {'*': 50, '/': 50, '%':50, '+': 40, '-': 40,
            'sin': HIGHEST_PREC, 'sqrt': HIGHEST_PREC, 'pow': HIGHEST_PREC,   # include special functions like these
            '(': 0, ')':1, ',': 5, '=': 10,
            'EOL':0}

        # denotes the number of arguments needed when that function is performed.
        self.args_needed =\
            {'*': 2, '/': 2, '%':2, '+': 2, '-': 2, '=': 2,
            'sin':1, 'pow':2, 'EOL': 0}

        self.functions = {'sin':1, 'pow':2}

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
        
        if not self.should_parse(tk_list):
            return None

        op_stack = []
        num_stack = []

        # op_s_len and the num_stack length get reset on encountering '(' or ','. See note 3
        stack_lengths = [[0, 0]]
        OP_ST = 0
        NUM_ST = 1
        op_stack_length = 0
        num_stack_length = 0

        # Use this to figure out whether not enough operands have been
        # pushed for the function to work.
        args_count_stack = [] 

        precedence = self.precedence

        i = 0
        while i < len(tk_list):
            tk_type, value = tk_list[i]

            if tk_type == 'NUM':
                num_stack.append(value)
                stack_lengths[-1][NUM_ST] = stack_lengths[-1][NUM_ST] + 1
            else:
                if tk_type == 'ID':
                    if value in self.functions:
                        tk_type = value
                    else:
                        # found a variable, go to next iteration.
                        num_stack.append(value)
                        stack_lengths[-1][NUM_ST] = stack_lengths[-1][NUM_ST] + 1
                        i = i + 1
                        continue

                if tk_type == '(':
                    op_stack.append(tk_type)
                    stack_lengths.append([0, 0])
                    i = i + 1
                    continue

                while op_stack and precedence[tk_type] <= precedence[op_stack[-1]]\
                    and op_stack[-1] in self.args_needed\
                    and stack_lengths[-1][NUM_ST] >= self.args_needed[op_stack[-1]]: # TODO bug in f(1, 2)
                    # See note 4 for op_stack[-1] in self.args_needed
                    # When I am looking at the current operand token,
                    # if it has a lower precedence then the topmost thing
                    # on the operand stack, keep popping off the num and op stacks
                    # and evaluate and push
                    operation = op_stack.pop()
                    stack_lengths[-1][OP_ST] = stack_lengths[-1][OP_ST] - 1

                    if operation in self.functions:
                        if args_count_stack[-1] == self.args_needed[operation]\
                            or (args_count_stack[-1] == 1 and self.args_needed[operation] == 0):
                            args_count_stack.pop()
                        else:
                            print 'Incorrect number of arguments to the function:', operation, '\nNeeded',\
                                self.args_needed[operation], 'but found', args_count_stack[-1]
                            return None


                    if operation == '=':
                        # See note 1 from notes.md, for why '=' is being tested
                        # here annd not in perform_operation
                        was_success, res = self.assign_and_terminate(num_stack)
                        if was_success:
                            num_stack.append(res)
                            i = i + 1
                            continue
                        else:
                            return None


                    # Now for other operations, pass in a list of operand values
                    operands = []
                    was_success = self.fetch_operands(num_stack, self.args_needed[operation], operands)
                    if not was_success:
                        return None
                    
                    stack_lengths[-1][NUM_ST] = stack_lengths[-1][NUM_ST] - self.args_needed[operation]
                    was_success, new_val = self.perform_operation(operands, operation)

                    if not was_success:
                        return None

                    num_stack.append(new_val)
                    stack_lengths[-1][NUM_ST] = stack_lengths[-1][NUM_ST] + 1


                if (tk_type == '-' or tk_type == '+')\
                    and (stack_lengths[-1][OP_ST] >= stack_lengths[-1][NUM_ST]):
                    # This solves the a  = -2 problem. See note 3
                    print 'called - + converter'
                    if tk_type == '-': 
                        num_stack.append(-1)
                        stack_lengths[-1][NUM_ST] = stack_lengths[-1][NUM_ST] + 1
                        tk_type = '*'
                    else:
                        i = i + 1
                        continue

                # At this point, either the operand stack is empty, or the top most
                # operand has a precedence lower than the newest operand.
                if tk_type == ')':
                    # The thing we stopped on must be '(', otherwise mismatch
                    if not op_stack or op_stack[-1] != '(':
                        print 'Mismatched parens.'
                        return None
                    op_stack.pop()

                    lengths = stack_lengths.pop()
                    if lengths[OP_ST] != 0:
                        print 'Syntax error!'
                        return None
                    stack_lengths[-1][NUM_ST] = stack_lengths[-1][NUM_ST] + lengths[NUM_ST]

                elif tk_type == ',':
                    if not args_count_stack:
                        print '"," must appear to separate function arguments.'
                        return None

                    args_count_stack[-1] = args_count_stack[-1] + 1
                    stack_lengths[-2][NUM_ST] += stack_lengths[-1][NUM_ST]
                    stack_lengths[-1] = [0, 0] # reset their lengths, not push a new frame
                    # We don't push ',' on to the stack.
                else:
                    if tk_type in self.functions:
                        args_count_stack.append(1)
                    op_stack.append(tk_type)
                    stack_lengths[-1][OP_ST] = stack_lengths[-1][OP_ST] + 1

            i = i + 1

        return self.check_num_stack_errors_and_return(num_stack)


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

        if arg_index != num_args - 1 and not (arg_index == 0 and num_args == 0):
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
        op_stack_length = 0
        num_stack_length = 0


        def_stack = [] # will hold the polish notation
        args_count_stack = [] # NOT to confuse with formal arguments, this structure is
                                # used to keep track of functions appearing within
        precedence = self.precedence

        while i < len(tk_list):
            tk_type, value = tk_list[i]
            if tk_type == 'NUM':
                pseudo_num_stack.append(('C', value)) # a constant
                num_stack_length = num_stack_length + 1
            else:
                if tk_type == 'ID':
                    if value in self.functions:
                        tk_type = value
                    else:
                        pseudo_num_stack.append(('A', value)) # argument
                        num_stack_length = num_stack_length + 1
                        i = i + 1
                        continue

                if tk_type == '(':
                    op_stack.append(tk_type)
                    num_stack_length = 0
                    op_stack_length = 0
                    i = i + 1
                    continue

                if (tk_type == '-' or tk_type == '+') and (op_stack_length >= num_stack_length):

                    pseudo_num_stack.append(('C', -1) if tk_type == '-' else ('C', 1))
                    num_stack_length = num_stack_length + 1
                    tk_type = '*'

                while op_stack and op_stack[-1] in self.args_needed\
                    and precedence[tk_type] <= precedence[op_stack[-1]]:
                    operation = op_stack.pop()
                    op_stack_length = op_stack_length - 1

                    if len(pseudo_num_stack) < self.args_needed[operation]:
                        print 'Not enough arguments to the function:', operation, '\nNeeded',\
                            self.args_needed[operation], 'but found', len(pseudo_num_stack)
                        return FAILURE

                    if operation in self.functions:
                        if args_count_stack[-1] == self.args_needed[operation]\
                            or (args_count_stack[-1] == 1 and self.args_needed[operation] == 0):
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

                    num_stack_length = num_stack_length - self.args_needed[operation]

                    def_stack.append(('O', operation))
                    pseudo_num_stack.append(('C', '$'))
                    num_stack_length = num_stack_length + 1
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
                    
                    args_count_stack[-1] = args_count_stack[-1] + 1
                    num_stack_length = 0
                    op_stack_length = 0
                else:
                    if tk_type in self.functions:
                        args_count_stack.append(1)
                    op_stack.append(tk_type)
                    op_stack_length = op_stack_length + 1
            i = i + 1

        if pseudo_num_stack:
            if len(pseudo_num_stack) > 1:
                print 'Not enough operators?'
                return FAILURE
            
            self.functions[func_name] = num_args
            self.precedence[func_name] = HIGHEST_PREC
            self.args_needed[func_name] = num_args
            if not def_stack:
                typ, val = pseudo_num_stack.pop()
                if typ == 'C':
                    def_stack.append(('C', val))
                else:
                    def_stack.append(('A', args[val]))
            self.user_functions[func_name] = def_stack

            return SUCCESS
        
        print 'Faulty expression in function definition!'
        return FAILURE


    def fetch_operands(self, num_stack, num_operands, operands):
        """
        num_stack is the num_stack in use in the parse method
        num_operands is the number of operands to fetch
        operands is the list that the operands will be added to, in REVERSE order
        """
        for j in xrange(num_operands):
            oper = num_stack.pop()
            if type(oper) == str:
                if oper in self.variables:
                    # The operands are being passed in reverse order
                    operands.append(self.variables[oper])
                else:
                    print 'The variable', oper, 'has not been defined.'
                    return FAILURE
            else:
                operands.append(oper)

        return SUCCESS


    def check_num_stack_errors_and_return(self, num_stack):
        """
        Method checks to see if the num_stack has been messed up:
        1) too many things still on the num stack (only one should be there)
        2) an undefined variable is on the num_stack
        """
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


    def should_parse(self, tk_list):
        """
        Reads the first token and decides whether the expression should be parsed. It
        shoud NOT be parsed when a print, help or def command is issued.
        """
        if len(tk_list) > 0:
            if tk_list[0][1] == 'help':
                miscell.print_help()
                return False
            if tk_list[0][1] == 'print':
                print 'Printing variables:'
                for key, value in self.variables.iteritems():
                    print key, '=', value
                print '\nDefined functions:'
                for key, value in self.functions.iteritems():
                    print 'The function', key, 'requires', value, 'arguments'
                return False
            if tk_list[0][1] == 'def':
                was_success = self.parse_definition(tk_list)
                if was_success:
                    print 'Function defined.'
                return False

        return True


    def assign_and_terminate(self, num_stack):
        val2 = num_stack.pop()
        val1 = num_stack.pop()
        if type(val1) == str:
            if type(val2) == str:
                if val2 in self.variables:
                    self.variables[val1] = self.variables[val2]
                    return SUCCESS, self.variables[val2]
                else:
                    print 'The variable', val2, 'has not been defined.'
                    return FAILURE, None
            else:
                self.variables[val1] = val2
                return SUCCESS, val2
        else:
            print 'Cannot assign a value to a non-variable.'
            return FAILURE, None
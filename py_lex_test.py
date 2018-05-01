def is_numeric(c):
    return c >= '0' and c <= '9'

def is_alpha(c):
    return c >= 'A' and c <= 'Z' and\
        c >= 'a' and c <= 'a'

def is_alphanumeric(c):
    return c >= 'A' and c <= 'Z' and\
        c >= 'a' and c <= 'a' and\
        c >= '0' and c <= '9'

def is_special(c):
    return c == '*' or c == '/' or\
        c == '+' or c == '-' or\
        c == '(' or c == ')'


# have a lexer class that rips tokens out and gives me one at a time
class MyLexer():
    def __init__(self, in_str='26'):
        self.in_str = in_str
        self.token_list = []

    def get_token_list(self):
        if not self.token_list:
            self._process_line()
        return self.token_list  # This could be dangerous, shall I clone it instead? TODO

    def get_token(self):
        if not self.token_list:
            self._process_line()
        item = self.token_list.pop(0)    
        return item

    def _process_line(self):
        # actually go through a line until you hit the new line character
        # add things into the token list

        if not self.in_str:
            self.token_list.append(('EOF', None))
            return

        length = len(self.in_str)
        i = 0
        while i < length:
            if is_numeric(self.in_str[i]):
                # It is a number, grab the entire number.
                num = 0
                while i < length and is_numeric(self.in_str[i]):
                    num = num * 10 + int(self.in_str[i])
                    i = i + 1

                self.token_list.append(('NUM', num))
            
            elif is_alpha(self.in_str[i]):
                # Requires variables to start with a letter. After that anything is fine
                # other than operands and spaces
                start_index = i
                while i < length and is_alphanumeric(self.in_str[i]):
                    i = i + 1
                # At this point, i points to the first next non-alphanumeric character
                self.token_list.append(('VAR', self.in_str[start_index:i]))
            elif is_special(self.in_str[i]):
                self.token_list.append((self.in_str[i], None))
                i = i + 1
            else:
                # Eat up whitespace and other junk
                i = i + 1

        self.token_list.append(('EOF', None))
        self.in_str = None
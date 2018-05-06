def is_numeric(c):
    return c >= '0' and c <= '9'

def is_alpha(c):
    return (c >= 'A' and c <= 'Z') or\
        (c >= 'a' and c <= 'z')

def is_alphanumeric(c):
    return (c >= 'A' and c <= 'Z') or\
        (c >= 'a' and c <= 'z') or\
        (c >= '0' and c <= '9')

def is_special(c):
    return c == '*' or c == '/' or\
        c == '+' or c == '-' or\
        c == '(' or c == ')' or\
        c == '=' or c == ','


# have a lexer class that rips tokens out and gives me one at a time
class MyLexer():
    def __init__(self):
        self.token_list = []

    def get_token_list(self, in_str):
        # Will return whether success or failure, and a corresponding list
        return self._process_line(in_str)

    def get_token(self):
        if not self.token_list:
            self.token_list = self._process_line('') # What the heck should this thing's args be 
        return self.token_list.pop()

    def _process_line(self, in_str):
        # actually go through a line until you hit the new line character
        # add things into the token list

        token_list = []

        if not in_str:
            token_list.append(('EOL', None))
            return token_list

        length = len(in_str)
        i = 0
        while i < length:
            if is_numeric(in_str[i]):
                # It is a number, grab the entire number.
                num = 0
                while i < length and is_numeric(in_str[i]):
                    num = num * 10 + int(in_str[i])
                    i = i + 1

                token_list.append(('NUM', float(num)))
            
            elif is_alpha(in_str[i]):
                # Requires variables to start with a letter. After that anything is fine
                # other than operands and spaces
                start_index = i
                while i < length and is_alphanumeric(in_str[i]):
                    i = i + 1
                # At this point, i points to the first next non-alphanumeric character
                token_list.append(('ID', in_str[start_index:i]))

            elif is_special(in_str[i]):
                token_list.append((in_str[i], None))
                i = i + 1

            else:
                # Eat up whitespace and other junk
                i = i + 1

        token_list.append(('EOL', None))
        return token_list
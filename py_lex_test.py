# have a lexer class that rips tokens out and gives me one at a time
class MyLexer():
    def __init__(self, in_str='9 + 9 * 8'):
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
        i = 0
        num = 0 # use this guy for number tokens
        processing_num = False
        if not self.in_str:
            self.token_list.append(('EOF', None))
            return

        for i in xrange(len(self.in_str)):
            if self.in_str[i] >= '0' and self.in_str[i] <= '9':
                processing_num = True
                num = num * 10 + int(self.in_str[i])
            else:
                if processing_num:
                    # If it was collecting a number until this point, put it
                    # into the tuple and send it.
                    self.token_list.append(('NUM', num))
                    processing_num = False
                    num = 0
                if self.in_str[i] == ' ' or self.in_str[i] == '\t':
                    continue

                self.token_list.append((self.in_str[i], None))

        if processing_num:
            self.token_list.append(('NUM', num))

        self.token_list.append(('EOF', None))
        self.in_str = None
import enum
import sys

# Token Types class:
class Token_type(enum.Enum):
	EOF = -1
	NEWLINE = 0
	NUMBER = 1
	IDENT = 2
	STRING = 3
	# Keywords.
	LABEL = 101
	GOTO = 102
	PRINT = 103
	INPUT = 104
	LET = 105
	IF = 106
	THEN = 107
	ENDIF = 108
	WHILE = 109
	REPEAT = 110
	ENDWHILE = 111
	# Operators.
	EQ = 201  
	PLUS = 202
	MINUS = 203
	ASTERISK = 204
	SLASH = 205
	EQEQ = 206
	NOTEQ = 207
	LT = 208
	LTEQ = 209
	GT = 210
	GTEQ = 211

class Token:
    def __init__(self, token_kind, token_text):
        self.kind = token_kind
        self.text = token_text
    @staticmethod

    def check_if_keyword(token_text):
        for it in Token_type:
            if it.name == token_text and it.value >= 100 and it.value < 200:
                return it
        return None


# Lexer class:

class Lexer:
    def __init__(self, source):
        self.source = source
        self.cur_char = ""
        self.cur_ind = -1
        self.next_char()

    def abort(self, message):
        sys.exit("Lexing error." + message)

    def next_char(self):
        self.cur_ind += 1
        if self.cur_ind >= len(self.source):
            self.cur_char = '\0'
        else:
            self.cur_char = self.source[self.cur_ind]

    def peek(self):
        if self.cur_ind >= len(self.source) - 1:
            return "\0"
        else:
            return self.source[self.cur_ind+1]

    def skip_white_space(self):
        while self.cur_char == ' ' or self.cur_char == '\t' or self.cur_char == '\r':
            self.next_char()

    def skip_comments(self):
        if self.cur_char == '#':
            while self.cur_char != '\0' and self.cur_char != '\n':
                self.next_char()

    def get_token(self):
        self.skip_white_space()
        self.skip_comments()
        token = None
        if self.cur_char == '+':
            token = Token(Token_type.PLUS, self.cur_char)

        elif self.cur_char == '-':
            token = Token(Token_type.MINUS, self.cur_char)

        elif self.cur_char == '*':
            token = Token(Token_type.ASTERISK, self.cur_char)

        elif self.cur_char == '/':
            token = Token(Token_type.SLASH, self.cur_char)

        elif self.cur_char == '\n':
            token = Token(Token_type.NEWLINE, self.cur_char)

        elif self.cur_char == '\0':
            token = Token(Token_type.EOF, '')

        elif self.cur_char == '=':
            last_char = self.cur_char
            if self.peek() == '=':
                self.next_char()
                token = Token(Token_type.EQEQ, last_char+self.cur_char)
            else:
                token = Token(Token_type.EQ, last_char)

        elif self.cur_char == '>':
            last_char = self.cur_char
            if self.peek() == '=':
                self.next_char()
                token = Token(Token_type.GTEQ, last_char+self.cur_char)
            else:
                token = Token(Token_type.GT, last_char)

        elif self.cur_char == '<':
            last_char = self.cur_char
            if self.peek() == '=':
                self.next_char()
                token = Token(Token_type.LTEQ, last_char+self.cur_char)
            else:
                token = Token(Token_type.LT, last_char)

        elif self.cur_char == '!':
            last_char = self.cur_char
            if self.peek() == '=':
                self.next_char()
                token = Token(Token_type.NOTEQ, last_char+self.cur_char)
            else:
                self.abort('Expected !, got !'+self.peek())

        elif self.cur_char == '\"':
            self.next_char()
            start_pos = self.cur_ind
            while self.cur_char != '\"':
                if self.cur_char == '\r' or self.cur_char == '\n' or self.cur_char == '\t' or self.cur_char == '\\' or self.cur_char == '%':
                    self.abort("Illegal characters in the string")
                self.next_char()
            token_text = self.source[start_pos : self.cur_ind]
            token = Token(Token_type.STRING, token_text)


        elif self.cur_char.isdigit():
            start_pos = self.cur_ind

            while self.peek().isdigit():
                self.next_char()

            if self.peek() == '.':
                self.next_char()

                if not self.peek().isdigit():
                    self.abort('Illegal character in number')

                while self.peek().isdigit():
                    self.next_char()

            token_text = self.source[start_pos : self.cur_ind+1]
            token = Token(Token_type.NUMBER, token_text)

        elif self.cur_char.isalpha():
            start_pos = self.cur_ind
            while self.peek().isalnum():
                self.next_char()
            token_text = self.source[start_pos : self.cur_ind+1]
            keyword = Token.check_if_keyword(token_text)
            if keyword == None:
                token = Token(Token_type.IDENT, token_text)
            else:
                token = Token(keyword, token_text)
        else:
            self.abort("Unknow token: " + self.cur_char)
        self.next_char()
        return token





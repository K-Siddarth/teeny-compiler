from lexer import *

import sys

class Parser:
    def __init__(self, lexer, emitter):
        self.lexer = lexer
        self.emitter = emitter

        self.labels_declared = set() # variables declered till now
        self.labels_gotoed = set() # gotos declared till now
        self.symbols = set() # variabled declared till now

        self.cur_token = None
        self.peek_token = None
        self.next_token() # makes cur_token = peek token (None), peek token = get_token
        self.next_token() # makes cur_token = peek token (lexer_token[0]), peek token = get_token() => token[1]




    def next_token (self):
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.get_token()

    def abort(self, message):
        sys.exit("Error."+message)

    def check_token (self, kind):
        if self.cur_token != None:
            return kind == self.cur_token.kind

    def check_peek(self, kind):
        if self.peek_token != None:
            return self.peek_token.kind == kind


    def match(self, kind):
        if self.cur_token == None:
            self.abort('Parsing error')
        if self.cur_token.kind != kind:
            self.abort('Expected' + kind.name + ', got ' + self.cur_token.text)
        self.next_token()

    def nl(self):
        # print("NEWLINE")

        self.match(Token_type.NEWLINE)

        while self.check_token(Token_type.NEWLINE):
            self.next_token()

    def is_comparision_operator(self):
        return self.check_token(Token_type.GT) or self.check_token(Token_type.LT) or self.check_token(Token_type.GTEQ) or self.check_token(Token_type.LTEQ) or self.check_token(Token_type.EQEQ) or self.check_token(Token_type.NOTEQ)

    def primary(self):
        if self.cur_token == None:
            self.abort('Parsing error')

        # print("PRIMARY" + "(" + self.cur_token.text+ ")") 

        if self.cur_token == None:
            self.abort('None cur_token in Primary')

        if self.check_token(Token_type.NUMBER):
            self.emitter.emit(self.cur_token.text)
            self.next_token()

        elif self.check_token(Token_type.IDENT):
            if self.cur_token.text not in self.symbols:
                self.abort("Referencing variable before assignment: " + self.cur_token.text)
            self.emitter.emit(self.cur_token.text)
            self.next_token()
        else:
            self.abort("Unexpected token at " + self.cur_token.text)

    def unary(self):
        # print("UNARY") 


        if self.cur_token == None:
            self.abort('None cur_token in unary')

        if self.check_token(Token_type.PLUS) or self.check_token(Token_type.MINUS):
            self.emitter.emit(self.cur_token.text)
            self.next_token()
        self.primary()

    def term(self):
        # print("TERM") 

        self.unary()

        if self.cur_token == None:
            self.abort('None cur_token in term')

        while self.check_token(Token_type.SLASH) or self.check_token(Token_type.ASTERISK):
            self.emitter.emit(self.cur_token.text)
            self.next_token()
            self.unary()

    def expression(self):
        # print("EXPRESSION") 

        self.term()
        
        if self.cur_token == None:
            self.abort('None cur_token in expression')

        while self.check_token(Token_type.PLUS) or self.check_token(Token_type.MINUS):
            self.emitter.emit(self.cur_token.text)
            self.next_token()
            self.term()

    def comparision(self):
        # print("COMPARISION")

        if self.cur_token == None:
            self.abort('Parsing error')

        self.expression()

        if self.is_comparision_operator():
            self.emitter.emit(self.cur_token.text)
            self.next_token()
            self.expression()
        else:
            self.abort('Expected comparision operator at: ' + self.cur_token.text)

        while self.is_comparision_operator():
            self.emitter.emit(self.cur_token.text)
            self.next_token()
            self.expression()



    def statement(self):
        if self.cur_token == None:
            self.abort('Parsing error')

        if self.check_token(Token_type.PRINT):
            # print("STATEMENT-PRINT")
            self.next_token()


            if self.check_token(Token_type.STRING):
                # emitting plain string directly into file
                self.emitter.emit_line('printf(\"' + self.cur_token.text + '\\n\");')
                self.next_token()
            else:
                self.emitter.emit('printf(\"%.2f\\n\", (float)(')
                self.expression()
                self.emitter.emit_line('));')

        elif self.check_token(Token_type.IF):
            # print("STATEMENT-IF")
            self.next_token()
            self.emitter.emit('if (')
            self.comparision()

            self.match(Token_type.THEN)
            self.nl()
            self.emitter.emit_line(')\n{')

            while not self.check_token(Token_type.ENDIF):
                self.statement()
            self.next_token()
            self.emitter.emit_line('}')

        elif self.check_token(Token_type.WHILE):
            # print("STATEMENT-WHILE")
            self.next_token()
            self.emitter.emit('while (')
            self.comparision()

            self.match(Token_type.REPEAT)
            self.nl()
            self.emitter.emit_line(')\n{')

            while not self.check_token(Token_type.ENDWHILE):
                self.statement()
            self.match(Token_type.ENDWHILE)
            self.emitter.emit_line('}')

        elif self.check_token(Token_type.LABEL):
            # print("STATEMENT-LABEL")
            self.next_token()
            if self.cur_token.text in self.labels_declared:
                self.abort("Label already exists" + self.cur_token.text)

            self.labels_declared.add(self.cur_token.text)
            self.emitter.emit_line(self.cur_token.text + ':')
            self.match(Token_type.IDENT)

        elif self.check_token(Token_type.GOTO):
            # print("STATEMENT-GOTO")
            self.next_token()
            self.labels_gotoed.add(self.cur_token.text)
            self.match(Token_type.IDENT)
            self.emitter.emit_line('goto ' + self.cur_token.text + ';')

        elif self.check_token(Token_type.LET):
            # print("STATEMENT-LET")
            self.next_token()
            
            if self.cur_token.text not in self.symbols:
                self.symbols.add(self.cur_token.text)
                self.emitter.header_line('float ' + self.cur_token.text + ';')

            self.emitter.emit(self.cur_token.text + '=')
            self.match(Token_type.IDENT)
            self.match(Token_type.EQ)

            self.expression()
            self.emitter.emit_line(';')

        elif self.check_token(Token_type.INPUT):
            # print("STATEMENT-INPUT")
            self.next_token()
            if self.cur_token.text not in self.symbols:
                self.emitter.header_line('float ' + self.cur_token.text + ';')
                self.symbols.add(self.cur_token.text)

            self.emitter.emit_line('if (0 == scanf(\"%f\", &' + self.cur_token.text +  '))\n{')
            self.emitter.emit_line(self.cur_token.text + '=0;')
            self.emitter.emit_line('scanf(\"%*s\");\n}')

            self.match(Token_type.IDENT)
        else:
            self.abort("Invalid statement at: " + self.cur_token.text + "(" + self.cur_token.kind.name + ")")

        self.nl()


    def program(self):
        print('PROGRAM')
        self.emitter.header_line('#include <stdio.h>')
        self.emitter.header_line('int main()\n{')

        while self.check_token(Token_type.NEWLINE):
            self.next_token()

        while not self.check_token(Token_type.EOF):
            self.statement()

        self.emitter.emit_line('return 0;')
        self.emitter.emit_line('}')

        for goto in self.labels_gotoed:
            if goto not in self.labels_declared:
                self.abort('GOTO to undeclared label ' + '(' + goto + ')')

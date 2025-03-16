from lexer import *
from parser import *
from emitter import *
import sys

def print_tokens(lexer, source):
    lexer = Lexer(source)
    token = lexer.get_token()
    while (token.kind != Token_type.EOF):
        print(token.kind)
        token = lexer.get_token()

def main():
    # source = "IF 9.123 #foo*THEN/"
    print("My compiler starting: ")
    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as input")
    with open(sys.argv[1], 'r') as input_file:
        source = input_file.read()

    lexer = Lexer(source)
    emitter = Emitter("out.c")
    parser = Parser(lexer, emitter)

    parser.program()
    emitter.write_file()
    print("Parsing complete")
main()

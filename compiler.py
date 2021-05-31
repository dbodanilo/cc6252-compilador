"""
Danilo Bizarria
Kaike Rodrigues
Markel Duarte
Matheus Ferreira
Rafael Lino
"""

from sys import stdin
from symbol import SymbolTable
from lexer import Lexer
from parser import Parser
from backend import PythonGenerator


def get_tokens(lexer):
    tokens = []

    # consumia primeiro token 
    # sem inserir na lista
#    token = lexer.get_token()
    for token in iter(lexer):
#    while(lexer.has_next_token()):
#        token = lexer.get_token()
        tokens.append(token)
    return tokens


def print_tokens(tks):
    print("[")
    for tk in tks:
        print(str(tk), end=",\n")
    
    print("]")


#code = input()
code = stdin.read()
#print(code)
symbolTable = SymbolTable()
#print(symbolTable)

#lex = Lexer(code, symbolTable)
#
#tokens = get_tokens(lex)
#print_tokens(tokens)
#print(str(lex.symbolTable))

lexer = Lexer(code, symbolTable)

parser = Parser(lexer, symbolTable)

syntaxTree = parser.parse()
#print(str(syntaxTree))
#print(str(parser.symbolTable))

if not parser.has_error and not parser.has_semantic_error:
    generator = PythonGenerator()
    generator.generate(syntaxTree)



from sys import stdin
from symbol import SymbolTable
from lexer import Lexer
from parser import Parser

code = stdin.read()
symbolTable = SymbolTable()

lex = Lexer(code, symbolTable)

par = Parser(lex, symbolTable)

print(str(par.parse()))

# def getTokens(lexer):
#     tokenV = []
# 
#     # consumia primeiro token 
#     # sem inserir na lista
# #    token = lexer.get_token()
#     while(lexer.has_next_char()):
#         token = lexer.get_token()
#         tokenV.append(token)
#     return tokenV


# tokens = getTokens(lex)

# print("[")
# for tk in tokens:
#     print(str(tk), end=",\n")
# 
# print("]")
# print(str(lex.symbolTable))


"""
Danilo Bizarria
Kaike Rodrigues
Markel Duarte
Matheus Ferreira
Rafael Lino
"""

"""
# Parser(self, Lexer):
#     while(Lexer.hasNextToken()):

#         # trata Token

# Int a = 2;

# [
#     ("Int", TYPE),
#     ("a", IDENTIFIER),
#     ("=", EQUAL),
#     ("2", NUMBER)
# ]

int a = 10;

Symbol(Token tk, Type )

Token("a", IDENTIFIER, ...)
type 
"""

from sys import stdin

import tekken

from tekken import Token
from tekken import TokenType
from symbol import Symbol
from symbol import SymbolTable


#code = input()
code = stdin.read()
symbolTable = SymbolTable()
class Lexer:

    def __init__(self, code, symbolTable):
        self.code = code
        self.symbolTable = symbolTable
        self.tokens = []
        self.tokenStart = 0
        self.nextIndex = 0
        self.line = 1

        self.cases = {
            '(': lambda: self.push_token(TokenType.LEFT_PAREN, '('),
            ')': lambda: self.push_token(TokenType.RIGHT_PAREN, ')'),
            '{': lambda: self.push_token(TokenType.LEFT_BRACE, '{'),
            '}': lambda: self.push_token(TokenType.RIGHT_BRACE, '}'),
            ',': lambda: self.push_token(TokenType.COMMA, ','),
            '.': lambda: self.push_token(TokenType.DOT, '.'),
            '-': lambda: self.push_token(TokenType.MINUS, '-'),
            '+': lambda: self.push_token(TokenType.PLUS, '+'),
            ';': lambda: self.push_token(TokenType.SEMICOLON, ';'),
            '*': lambda: self.push_token(TokenType.STAR, '*'),
            '?': lambda: self.push_token(TokenType.QUESTION, '?'),
            ':': lambda: self.push_token(TokenType.COLON, ':'),
                
            '/': lambda: self.push_token(TokenType.NOT_EQUAL, '/=') if self.is_next_char("=") else self.push_token(TokenType.SLASH, '/'),
            '=': lambda: self.push_token(TokenType.EQUAL_EQUAL, '==') if self.is_next_char("=") else self.push_token(TokenType.EQUAL, '='),
            '>': lambda: self.push_token(TokenType.GREATER_EQUAL, '>=') if self.is_next_char("=") else self.push_token(TokenType.GREATER, '>'),
            '<': lambda: self.push_token(TokenType.LESS_EQUAL, '<=') if self.is_next_char("=") else self.push_token(TokenType.LESS, '<'), 

            # ignore whitespace
            # todo: handle comments 
            ' ': lambda: self.switch_char()() if self.has_next_char() else None,
            '\n': lambda: self.next_line()() if self.has_next_char() else None,
            '"': lambda: self.push_string('"'),
            "'": lambda: self.push_string("'"),
        }
        
        # python excludes end in (start, end)
        for c_num in range(ord('0'), ord('9') + 1):
            self.cases[chr(c_num)] = lambda: self.push_number()

        for c_lower in range(ord('a'), ord('z') + 1):
            self.cases[chr(c_lower)] = lambda: self.push_char(TokenType.IDENTIFIER)

        for c_upper in range(ord('A'), ord('Z') + 1):
            self.cases[chr(c_upper)] = lambda: self.push_char(TokenType.TYPE)

        self.reserved = {
            # keywords
            "and": TokenType.AND,
            "break": TokenType.BREAK,
            "continue": TokenType.CONTINUE,
            "else": TokenType.ELSE,
            "for": TokenType.FOR,
            "if": TokenType.IF,
            "not": TokenType.NOT,
            "or": TokenType.OR,
            "return": TokenType.RETURN,
            "while": TokenType.WHILE,

            # built-in
            "false": TokenType.FALSE,
            "null": TokenType.NULL,
            "true": TokenType.TRUE,
        }        


    def advance_char(self):
        self.nextIndex += 1

#    def if_reserved(self, word, t_type):
      

    def push_char(self, tk_type):
        idx_start = self.nextIndex - 1
        while self.has_next_char() and self.peek_char().isalpha():
            self.advance_char()
        idx_end = self.nextIndex

        word = self.code[idx_start:idx_end] 

        tk_type = self.reserved.get(word, tk_type) 

#        tk_type = self.if_reserved(word, tk_type)

        return self.push_token(tk_type, word)

    def push_number(self):
        idx_start = self.nextIndex - 1
        while self.has_next_char() and self.peek_char().isdigit():
            self.advance_char()

        if(self.peek_char() == '.'):
            self.advance_char()
            while self.has_next_char() and self.peek_char().isdigit():
                self.advance_char()

        idx_end = self.nextIndex
        
        return self.push_token(TokenType.NUMBER, self.code[idx_start:idx_end])

    def push_string(self, delim):
        idx_start = self.nextIndex - 1
        while self.has_next_char() and self.peek_char() != delim:
            self.advance_char()
        if not self.has_next_char():
            return self.erro('String nao terminada')
        # get second delim
        self.advance_char()
        idx_end = self.nextIndex

        return self.push_token(TokenType.STRING, self.code[idx_start:idx_end])

    def push_token(self, tokenType, tokenChar):
        newToken = Token(self.line, tokenChar, tokenType)
        self.tokens.append(newToken)
        if tokenType == TokenType.TYPE or tokenType == TokenType.IDENTIFIER:
            sym = Symbol(newToken)
            self.symbolTable.insert(tokenChar, sym) 
        return newToken


    # iterator methods
    def __iter__(self):
        return self


    def __next__(self):
        return self.get_token()
   

    def has_next_char(self):
        return self.nextIndex < len(self.code)

    def peek_char(self):
        if not self.has_next_char():
            return None
        
        c = self.code[self.nextIndex]
        return c

    def next_char(self):
        if not self.has_next_char():
            return None
        
        c = self.code[self.nextIndex]
        self.nextIndex += 1
        return c


    def is_next_char(self, c):
        if not self.has_next_char():
            return False
       
        if self.code[self.nextIndex] == c:
            self.nextIndex += 1
            return True
        
        return False

    def next_line(self):
        self.line += 1

        if self.has_next_char():
            #print(self.code[self.nextIndex])
            return self.switch_char()
        else: 
            return lambda: None


    def switch_char(self):
        return self.cases.get(self.next_char(), self.erro)


    def get_current_char(self):
#        if self.has_next_char():
        return self.code[self.nextIndex - 1]
#        return 'EOF'


    def erro(self, msg = 'Caractere nao reconhecido'):
        c_char = 'EOF'
        if self.has_next_char():
            c_char = self.get_current_char()
           
        print(f'Linha {self.line} - {msg}: {c_char}')
        tokenError = Token(self.line, c_char, TokenType.ERROR)
        return tokenError

    def has_next_token(self):
        return self.has_next_char()    


    def get_token(self):
        tk_fun = self.switch_char()

#        token = tk_fun if tk_fun is None else tk_fun()
        token = tk_fun()

        # whitespace
        #if Token is None:
        #    token = self.get_token()

        return token

            

# if(x>0){a+=10;}

    # uso interno pelo Lexer
#    def hasNextChar(self):
#        return self.charIndex + 1 < len(self.code)

#    def nextChar(self):
#        c = self.code[self.charIndex]
#        self.charIndex += 1
#        return c

#print(code)
#print()

lex = Lexer(code, symbolTable)

def getTokens(lexer):
    tokenV = []

    # consumia primeiro token 
    # sem inserir na lista
#    token = lexer.get_token()
    while(lexer.has_next_char()):
        token = lexer.get_token()
        tokenV.append(token)
    return tokenV


tokens = getTokens(lex)

print("[")
for tk in tokens:
    print(str(tk), end=",\n")

print("]")
print(str(lex.symbolTable))

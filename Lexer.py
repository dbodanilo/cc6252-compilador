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


from enum import Enum


class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.tokenStart = 0
        self.nextIndex = 0
        self.line = 1


    # iterator methods
    def __iter__(self):
        return self


    def __next__(self):
        return self.get_token()
   

    def has_next_char(self):
        return self.nextIndex < len(code)


    def next_char(self):
        if not self.has_next_char():
            return None
        
        c = self.code[nextIndex]
        self.nextIndex += 1
        return c


    def is_next_char(self, c):
        if not self.has_next_char():
            return False
       
        if self.code[self.nextIndex] == c:
            self.nextIndex += 1
            return True
        
        return False


    def switch_char(self, c):
        cases = {
            '(': lambda: self.push_token(LEFT_PAREN),
            ')': lambda: self.push_token(RIGHT_PAREN),
            '{': lambda: self.push_token(LEFT_BRACE),
            '}': lambda: self.push_token(RIGHT_BRACE),
            ',': lambda: self.push_token(COMMA),
            '.': lambda: self.push_token(DOT),
            '-': lambda: self.push_token(MINUS),
            '+': lambda: self.push_token(PLUS),
            ';': lambda: self.push_token(SEMICOLON),
            '*': lambda: self.push_token(STAR),
            '?': lambda: self.push_token(QUESTION),
            ':': lambda: self.push_token(COLON),
                
            '/': lambda: self.push_token(NOT_EQUAL if is_next_char("=") else SLASH),
            '=': lambda: self.push_token(EQUAL_EQUAL if is_next_char("=") else EQUAL),
            '>': lambda: self.push_token(GREATER_EQUAL if is_next_char("=") else GREATER),
            '<': lambda: self.push_token(LESS_EQUAL if is_next_char("=") else LESS),
            ' ': lambda: None,
            '\n': lambda: self.line += 1
              return None
            '': None
        }

        return cases[c]


    def get_token(self):
        c = self.next_char()
        token = switch_char(c)
        
        # whitespace
        if Token is None:
            token = self.get_token()

        return token

            
    def getTokens(self):
        while(self.has_next_char()):
            c = self.next_char()
            return self.switch_char(c)

# if(x>0){a+=10;}

    # uso interno pelo Lexer
    def hasNextChar(self):
        return self.charIndex + 1 < len(self.code)

    def nextChar(self):
        c = self.code[self.charIndex]
        self.charIndex += 1
        return c

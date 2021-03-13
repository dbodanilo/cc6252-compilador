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

import TokenType


class Lexer:
    def __init__(self, code):
        self.code = code
        self.charIndex = 0
        self.line = 1

    # uso externo
    def hasNextToken(self):
        return False

    def nextToken(self):
        return None

    def switch_char(self, c):
        cases = {
                '(': None,
                ')': None,
                '{': None
                }
        return cases.get(c)

    def getTokens(self):
        while(self.hasNextChar()):
            c = self.nextChar()
            return self.switch_char(c)

# if(x>0){a+=10;}

    # uso interno pelo Lexer
    def hasNextChar(self):
        return self.charIndex + 1 < len(self.code)

    def nextChar(self):
        c = self.code[self.charIndex]
        self.charIndex += 1
        return c

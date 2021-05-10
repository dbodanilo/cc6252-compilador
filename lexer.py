"""
Danilo Bizarria
Kaike Rodrigues
Markel Duarte
Matheus Ferreira
Rafael Lino
"""

from tekken import Token
from tekken import TokenType
from symbol import Symbol
from symbol import SymbolTable

class Lexer:
    def __init__(self, code, symbolTable):
        self.code = code
        self.symbolTable = symbolTable
        self.tokens = []
        self.tokenStart = 0
        self.nextIndex = 0
        self.line = 1

        self.reserved = {
            # keywords
            "and": TokenType.AND,
            "break": TokenType.BREAK,
            "continue": TokenType.CONTINUE,
            "else": TokenType.ELSE,
            "for": TokenType.FOR,
            "if": TokenType.IF,
            "in": TokenType.IN,
            "not": TokenType.NOT,
            "or": TokenType.OR,
            "return": TokenType.RETURN,
            "while": TokenType.WHILE,

            # built-in
            "false": TokenType.FALSE,
            "null": TokenType.NULL,
            "true": TokenType.TRUE,
        }        

        self.cases = {
            '(': lambda: self.push_token(TokenType.LEFT_PAREN, '('),
            ')': lambda: self.push_token(TokenType.RIGHT_PAREN, ')'),
            '{': lambda: self.push_token(TokenType.LEFT_BRACE, '{'),
            '}': lambda: self.push_token(TokenType.RIGHT_BRACE, '}'),
            ',': lambda: self.push_token(TokenType.COMMA, ','),
            '.': lambda: self.push_token(TokenType.DOT, '.'),

            # handle comments "--"
            '-': self.push_minus,
            '+': lambda: self.push_token(TokenType.PLUS, '+'),
            ';': lambda: self.push_token(TokenType.SEMICOLON, ';'),
            '*': lambda: self.push_token(TokenType.STAR, '*'),
            '?': lambda: self.push_token(TokenType.QUESTION, '?'),
            ':': lambda: self.push_token(TokenType.COLON, ':'),
                
            '/': self.push_slash,
            '=': self.push_equal,
            '>': self.push_greater,
            '<': self.push_less, 

            # ignore whitespace
            # todo: handle comments 
            '\n': self.push_line,
            '\r': self.push_space,
            '\t': self.push_space,
            ' ':  self.push_space,
            '"': lambda: self.push_string('"'),
            "'": lambda: self.push_string("'"),
        }
        
        # python excludes end in range(start, end)
        for c_num in range(ord('0'), ord('9') + 1):
            self.cases[chr(c_num)] = self.push_number

        for c_lower in range(ord('a'), ord('z') + 1):
            self.cases[chr(c_lower)] = lambda: self.push_char(TokenType.IDENTIFIER)

        for c_upper in range(ord('A'), ord('Z') + 1):
            self.cases[chr(c_upper)] = lambda: self.push_char(TokenType.TYPE)


    def push_line(self):
        self.line += 1
        return self.push_space()


    def push_space(self):
        if self.has_next_char():
            return self.switch_char()()
        else: 
            return self.push_token(TokenType.EOF, "EOF")


    def push_slash(self):
        if self.is_next_char("="):
            return self.push_token(TokenType.NOT_EQUAL, '/=')  
        else: 
            return self.push_token(TokenType.SLASH, '/')


    def push_minus(self):
        if self.is_next_char("-"):
            return self.push_comment()  
        else: 
            return self.push_token(TokenType.MINUS, '-')


    def push_less(self):
        if self.is_next_char("="):
            return self.push_token(TokenType.LESS_EQUAL, '<=')  
        else: 
            return self.push_token(TokenType.LESS, '<')


    def push_greater(self):
        if self.is_next_char("="):
            return self.push_token(TokenType.GREATER_EQUAL, '>=')  
        else: 
            return self.push_token(TokenType.GREATER, '>')


    def push_equal(self):
        if self.is_next_char("="):
            return self.push_token(TokenType.EQUAL_EQUAL, '==')  
        else: 
            return self.push_token(TokenType.EQUAL, '=')


    def push_comment(self):
        while self.peek_char() != '\n':
            self.advance_char()

        return self.push_line()


    def push_char(self, tk_type):
        idx_start = self.nextIndex - 1
        c = self.peek_char()
        while self.has_next_char() and (c.isalnum() or c == "_"):
            self.advance_char()
            c = self.peek_char()

        idx_end = self.nextIndex

        word = self.code[idx_start:idx_end] 

        tk_type = self.reserved.get(word, tk_type) 

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
            return self.error()('Unterminated String')
        # get second delim
        self.advance_char()
        idx_end = self.nextIndex

        return self.push_token(TokenType.STRING, self.code[idx_start:idx_end])

    def push_token(self, tokenType, tokenChar):
        newToken = Token(self.line, tokenChar, tokenType)
        self.tokens.append(newToken)

        if tokenType in (TokenType.TYPE, TokenType.IDENTIFIER):
            sym = Symbol(newToken)
            self.symbolTable.insert(tokenChar, sym) 

        return newToken


    # iterator methods
    def __iter__(self):
        return self


    def __next__(self):
        if self.has_next_token():
            return self.get_token()
        else:
            raise StopIteration
   

    def has_next_char(self):
        return self.nextIndex < len(self.code)


    def advance_char(self):
        self.nextIndex += 1


    def peek_char(self):
        if not self.has_next_char():
            return None
        
        c = self.code[self.nextIndex]
        return c


    def next_char(self):
        c = self.peek_char()

        if c is not None:
            self.advance_char()

#        if not self.has_next_char():
#            return None
#        
#        c = self.code[self.nextIndex]
#        self.nextIndex += 1
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
        if self.has_next_char():
            current_char = self.next_char()
            return self.cases.get(current_char, self.error(current_char))
        
        return lambda: self.push_token(TokenType.EOF, "EOF")


    def get_current_char(self):
        # doesn't make sense, 
        # as current, not next char is to be returned
#        if self.has_next_char():
        if self.nextIndex > 0:
            return self.code[self.nextIndex - 1]

        # empty file
        return 'EOF'


    def error(self, c_char = 'EOF'):

        def log_error(msg = "Unrecognized Character"):
            print(f"Line {self.line}, Invalid Input: {msg} \'{c_char}\'")
#            tokenError = Token(self.line, c_char, TokenType.ERROR)
            # treat unrecognized char as whitespace
            return self.push_space()

        return log_error


    def has_next_token(self):
        return self.has_next_char()    


    def get_token(self):
        tk_fun = self.switch_char()

        token = tk_fun()

        return token


from tekken import TokenType
from parseTree import *

class Parser:
    def __init__(self, lexer, symbolTable):
        self.lexer = lexer
        self.current_token = self.lexer.get_token()
        self.symbolTable = symbolTable

    def parse(self):
#        return self.line()
        return self.expr()
    

    def line(self):
        # line = declaration
        # | (assignment , ";")
        # | conditional
        # | loopFor
        # | loopWhile
        # | function ;
        cases = {
                TokenType.TYPE: self.declaration,
                TokenType.IDENTIFIER: self.assignmentline,
                TokenType.IF: self.conditional,
                TokenType.FOR: self.loopfor,
                TokenType.WHILE: self.loopwhile
                }


    def assignmentline(self):
        _line = assignment()

        eat(TokenType.SEMICOLON)
        return LineNode(_line)


    def assignment(self):
        _assignment = identifier()
        
        while self.current_token.t_type == TokenType.EQUAL:
            left = _assignment
            op = self.current_token
            eat(TokenType.EQUAL)
#            if self.current_token.t_type in (TokenType.IDENTIFIER, TokenType.STRING, TokenType.NUMBER):
            right = self.factor()
#            else:
#                right = assignment()
            _assignment = BinOpNode(left, right, op)

        return _assignment


    def declaration(): 
        pass

 
    def expr(self):
        _expr = self.term()

# a + b + c ...
# _expr = ValueNode(a)
# _expr = BinOpNode(a, b, +)
# _expr = BinOpNode((a + b), c, +)

        while self.current_token.t_type in (TokenType.PLUS, TokenType.MINUS):
            left = _expr
            op = self.current_token
            self.eat(op.t_type)
            right = self.term()
            _expr = BinOpNode(left, right, op)

        return _expr


    def term(self):
        _term = self.factor() # ValueNode(10)

        while self.current_token.t_type in (TokenType.STAR, TokenType.SLASH):
            left = _term
            op = self.current_token
            self.eat(op.t_type)
            right = self.factor()
            _term = BinOpNode(left, right, op)

        return _term


    def factor(self):
        token = self.current_token
        _factor = None

        if token.t_type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            _factor = ValueNode(token)

        elif token.t_type == TokenType.LEFT_PAREN:
            self.eat(TokenType.LEFT_PAREN)
            _factor = self.expr()
            self.eat(TokenType.RIGHT_PAREN)

        return _factor


    def value():
        pass
        

    def error(self):
        print("Sintaxe inválida")


    def eat(self, token_type):
        if self.current_token.t_type == token_type:
            if self.lexer.has_next_token():
                self.current_token = self.lexer.get_token()
            else:
                self.current_token = None
        else:
            self.error()


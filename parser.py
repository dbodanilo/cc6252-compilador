from tekken import TokenType
from parseTree import *

class Parser:
    def __init__(self, lexer, symbolTable):
        self.lexer = lexer
        self.current_token = self.lexer.get_token()
#        print(self.current_token)
        self.symbolTable = symbolTable
        self.has_error = False


    def get_tokens(lexer):
        tokens = []
    
        # consumia primeiro token 
        # sem inserir na lista
    #    token = lexer.get_token()
        while(lexer.has_next_token()):
            token = lexer.get_token()
            tokens.append(token)
        return tokens


    def parse(self):
        nodeList = []
#        return self.line()
#        return self.expr()
        while self.current_token != TokenType.EOF and not self.has_error:
            nodeList.append(self.line())
        return nodeList
    

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
                #TokenType.FOR: self.loopfor,
                #TokenType.WHILE: self.loopwhile
                }
        return cases.get(self.current_token.t_type, self.error)()

    def conditional(self):
        self.eat(TokenType.IF)
        self.eat(TokenType.LEFT_PAREN)
        condition = self.expr()
        self.eat(TokenType.RIGHT_PAREN)
        ifBlock = self.block()
        elseBlock = None
        if self.current_token.t_type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            elseBlock = self.block()

        return IfNode(condition, ifBlock, elseBlock)

    def block(self):
        self.eat(TokenType.LEFT_BRACE)
        lineList = []
        while self.current_token.t_type != TokenType.RIGHT_BRACE:
            lineList.append(self.line())
        self.eat(TokenType.RIGHT_BRACE)
        
        return BlockNode(lineList) 


    
    def assignmentline(self):
        _line = assignment()

        self.eat(TokenType.SEMICOLON)
        return LineNode(_line)


    def assignment(self):
        _assignment = identifier()
        
        while self.current_token.t_type == TokenType.EQUAL:
            left = _assignment
            op = self.current_token
            self.eat(TokenType.EQUAL)
#            if self.current_token.t_type in (TokenType.IDENTIFIER, TokenType.STRING, TokenType.NUMBER):
            right = self.factor()
#            else:
#                right = assignment()
            _assignment = BinOpNode(left, right, op)

        return _assignment


    def declaration(self):
        firstToken = self.current_token
        self.eat(TokenType.TYPE)
        if self.current_token.t_type == TokenType.IDENTIFIER:
            left  = self.current_token
            self.eat(TokenType.IDENTIFIER)
            if self.current_token.t_type == TokenType.SEMICOLON:
                decl = DeclNode(firstToken, left, None)
                self.eat(TokenType.SEMICOLON)
                return decl
            self.eat(TokenType.EQUAL)
            #if self.current_token.t_type in (TokenType.NUMBER, TokenType.STRING, TokenType.TRUE, TokenType.FALSE, TokenType.NULL):
            #    right = self.current_token.t_type
            #    self.eat(right.t_type)
            #    decl = DeclNode(firstToken, left, right)
            #    self.eat(TokenType.SEMICOLON)
            #    return decl
            right = self.expr()
            self.eat(TokenType.SEMICOLON)
            return DeclNode(firstToken, left, right)

 
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

        if token.t_type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            _factor = ValueNode(token, token.name)

        elif token.t_type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            _factor = ValueNode(token, token.name)

        elif token.t_type == TokenType.NULL:
            self.eat(TokenType.NULL)
            _factor = ValueNode(token, None)
        
        elif token.t_type == TokenType.TRUE:
            self.eat(TokenType.TRUE)
            _factor = ValueNode(token, True)

        elif token.t_type == TokenType.FALSE:
            self.eat(TokenType.FALSE)
            _factor = ValueNode(token, False)

        elif token.t_type == TokenType.STRING:
            self.eat(TokenType.STRING)
            _factor = ValueNode(token, token.name)

        elif token.t_type == TokenType.LEFT_PAREN:
            self.eat(TokenType.LEFT_PAREN)
            _factor = self.expr()
            self.eat(TokenType.RIGHT_PAREN)

        return _factor


    def value():
        pass
        

    def error(self):
        self.has_error = True
        print("Sintaxe inválida")


    def eat(self, token_type):
        if self.current_token.t_type == token_type:
            print(self.current_token)
            if self.lexer.has_next_token():
                self.current_token = self.lexer.get_token()
            else:
                self.current_token = None
        else:
            self.error()


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
        while self.current_token.t_type != TokenType.EOF and not self.has_error:
            nodeList.append(self.line())
        return nodeList
    

    def line(self):
        # line = declaration
        #      | assignmentLine
        #      | conditional
        #      | loopFor
        #      | loopWhile
        cases = {
                TokenType.TYPE: self.declaration,
                TokenType.IDENTIFIER: self.assignmentLine,
                TokenType.IF: self.conditional,
                #TokenType.FOR: self.loopFor,
                #TokenType.WHILE: self.loopWhile
                }

        current_type = self.current_token.t_type

        linefun = cases.get(current_type, None)
        if linefun is None:
            msg = "expected one of: "
            for t_type in cases:
                msg += str(t_type)
            msg += "got {current_type}."
            error(msg)
        else:
            return linefun()

    def conditional(self):
        self.eat(TokenType.IF)
        self.eat(TokenType.LEFT_PAREN)
        condition = self.orExpr()
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
        while self.current_token.t_type != TokenType.RIGHT_BRACE and not self.has_error:
            lineList.append(self.line())
        self.eat(TokenType.RIGHT_BRACE)
        
        return BlockNode(lineList) 


    
    def assignmentLine(self):
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
        declType = self.current_token
        self.eat(TokenType.TYPE)
        if self.current_token.t_type == TokenType.IDENTIFIER:
            left  = self.current_token
            self.eat(TokenType.IDENTIFIER)
            if self.current_token.t_type == TokenType.SEMICOLON:
                decl = DeclNode(declType, left, None)
                self.eat(TokenType.SEMICOLON)
                return decl
            self.eat(TokenType.EQUAL)
            #if self.current_token.t_type in (TokenType.NUMBER, TokenType.STRING, TokenType.TRUE, TokenType.FALSE, TokenType.NULL):
            #    right = self.current_token.t_type
            #    self.eat(right.t_type)
            #    decl = DeclNode(declType, left, right)
            #    self.eat(TokenType.SEMICOLON)
            #    return decl
            right = self.expr()
            self.eat(TokenType.SEMICOLON)
            return DeclNode(declType, left, right)


    def orExpr(self):
        _or = self.andExpr()

        while self.current_token.t_type == TokenType.OR:
            left = _or
            op = self.current_token
            self.eat(TokenType.OR)
            right = self.andExpr()
            _or = BinOpNode(left, right, op)

        return _or

 
    def andExpr(self):
        _and = self.compExpr()

        while self.current_token.t_type == TokenType.AND:
            left = _and
            op = self.current_token
            self.eat(TokenType.AND)
            right = self.compExpr()
            _and = BinOpNode(left, right, op)

        return _and

 
    def compExpr(self):
        _comp = self.expr()

        while self.current_token.t_type in (TokenType.LESS, TokenType.GREATER, TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL, TokenType.EQUAL_EQUAL, TokenType.NOT_EQUAL):
            left = _comp
            op = self.current_token
            self.eat(op.t_type)
            right = self.expr()
            _comp = BinOpNode(left, right, op)

        return _comp

 
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
            _factor = self.compExpr()
            self.eat(TokenType.RIGHT_PAREN)

        return _factor


    def value():
        pass
        

    def error(self, msg = ""):
        self.has_error = True
        # end="" avoids new line in case of detailed message
        print("Invalid Syntax", end="")
        if len(msg) > 0:
            print(f": {msg}")
        else:
            # in case there's no message, print a new line
            print("")


    def eat(self, token_type):
        current_type = self.current_token.t_type
        if current_type == token_type:
            print(self.current_token)
            if self.lexer.has_next_token():
                self.current_token = self.lexer.get_token()
            else:
                self.current_token = None
        else:
            self.error(f"expected {token_type}, got {current_type}")


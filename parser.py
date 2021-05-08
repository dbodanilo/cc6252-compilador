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
        return BlockNode(nodeList)
    

    def line(self):
        # line = assignmentLine
        #      | conditional
        #      | declaration
        #      | loopFor
        #      | loopWhile
        #      | returnLine ;
        cases = {
                TokenType.IDENTIFIER: self.assignmentLine,
                TokenType.IF: self.conditional,
                TokenType.TYPE: self.declaration,
                TokenType.FOR: self.loopFor,
                TokenType.WHILE: self.loopWhile,
                TokenType.RETURN: self.returnLine,
                }

        current_type = self.current_token.t_type

        linefun = cases.get(current_type, None)
        if linefun is None:
            msg = "expected one of: "
            for t_type in cases:
                msg += f"{str(t_type)}, "
            msg += f"got {current_type}."
            self.error(msg)
        else:
            return linefun()


    def returnLine(self):
        # return r = a and b or c + d
        self.eat(TokenType.RETURN)
        
        returnValue = None
        if self.current_token.t_type != TokenType.SEMICOLON:
            returnValue = self.assignment()

        self.eat(TokenType.SEMICOLON)

        return ReturnNode(returnValue)


    def loopFor(self):
        self.eat(TokenType.FOR)
        self.eat(TokenType.LEFT_PAREN)

        decl = None
        if self.current_token.t_type == TokenType.TYPE:
            decl = self.declaration()
        elif self.current_token.t_type == TokenType.IDENTIFIER:
            decl = self.assignmentLine()
        
        condition = self.assignment()
        self.eat(TokenType.SEMICOLON)

        assign = self.assignment()
        self.eat(TokenType.RIGHT_PAREN)

        forBlock = self.block()

        return ForNode(decl, condition, assign, forBlock)


    def loopWhile(self):
        self.eat(TokenType.WHILE)
        self.eat(TokenType.LEFT_PAREN)
        condition = self.assignment()
        self.eat(TokenType.RIGHT_PAREN)
        whileBlock = self.block()

        return WhileNode(condition, whileBlock)


    def conditional(self):
        self.eat(TokenType.IF)
        self.eat(TokenType.LEFT_PAREN)
        condition = self.assignment()
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
        _line = self.assignment()

        self.eat(TokenType.SEMICOLON)
        return _line


    def assignment(self):
        # a < c = b;
        _assignment = self.orExpr()

        if self.current_token.t_type == TokenType.EQUAL:
            left = _assignment

            op = self.current_token
            self.eat(TokenType.EQUAL)

            right = self.assignment() 

            _assignment = BinOpNode(left, right, op)

        return _assignment


    def declaration(self):
        declType = self.current_token
        self.eat(TokenType.TYPE)

        left  = self.current_token
        self.eat(TokenType.IDENTIFIER)

        right = None
        if self.current_token.t_type == TokenType.EQUAL:    
            self.eat(TokenType.EQUAL)
            right = self.orExpr()

        # Bool f(Number x) { }
        # [Bool, Number f = (Number x) { } )
        elif self.current_token.t_type == TokenType.LEFT_PAREN:
            declType = [declType]
            right = self.function(declType)
              # declType.append(param_type)

        self.eat(TokenType.SEMICOLON)

        return DeclNode(declType, left, right)


    def function(self, types = []):
        self.eat(TokenType.LEFT_PAREN)
        params = []

        while self.current_token.t_type != TokenType.RIGHT_PAREN:
            params.append(self.param(types))
            if self.current_token.t_type == TokenType.COMMA:
                self.eat(TokenType.COMMA)

        self.eat(TokenType.RIGHT_PAREN)
        functionBlock = self.block()

        return FunctionNode(params, functionBlock)


    def param(self, types):
        paramType = self.current_token
        types.append(paramType)
        self.eat(TokenType.TYPE)

        left  = self.current_token
        self.eat(TokenType.IDENTIFIER)

        right = None
        if self.current_token.t_type == TokenType.EQUAL:    
            self.eat(TokenType.EQUAL)
            right = self.orExpr()

#        # Bool f(Number x) { }
#        # [Bool, Number f = (Number x) { } )
#        elif self.current.token.t_type == TokenType.LEFT_PAREN:
#            declType = [declType]
#            right = self.function(declType)
#              # declType.append(param_type)

        return DeclNode(paramType, left, right)


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
            _factor = self.orExpr()
            self.eat(TokenType.RIGHT_PAREN)

        return _factor

    
    def identifier(self):
        token = self.current_token
        self.eat(TokenType.IDENTIFIER)
        return ValueNode(token, token.name)


    def value(self):
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
#            print(self.current_token)
            if self.lexer.has_next_token():
                self.current_token = self.lexer.get_token()
            else:
                self.current_token = None
        else:
            self.error(f"expected {token_type}, got {current_type}")


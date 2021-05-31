"""
Danilo Bizarria
Kaike Rodrigues
Markel Duarte
Matheus Ferreira
Rafael Lino
"""
import sys
from tekken import TokenType, Token
from symbol import Symbol
from parseTree import *


class Parser:
    def __init__(self, lexer, symbolTable):
        self.lexer = lexer
        self.symbolTable = symbolTable
        self.current_token = self.lexer.get_token()
#        print(self.current_token)
        self.has_error = False
        self.has_semantic_error = False
        self.tokens = []


    def get_tokens(self):    
        for token in iter(self.lexer):
            self.tokens.append(token)

        return self.tokens


    def parse(self):
        lines = []

        while not self.has_error:
            current_line = self.line()

            if current_line is not None:
                lines.append(current_line)
            else:
                # EOF is the only cause for None
                break

        return BlockNode(lines)
    

    def line(self):
        cases = {
                TokenType.IDENTIFIER: self.assignmentLine,
                TokenType.IF: self.conditional,
                TokenType.TYPE: self.declaration,
                TokenType.FOR: self.loopFor,
                TokenType.WHILE: self.loopWhile,
                TokenType.RETURN: self.returnLine,

                # a single semicolon
                TokenType.SEMICOLON: self.emptyLine,

                # EOF
                TokenType.EOF: lambda: None,
                }

        token = self.current_token

        linefun = cases.get(token.t_type, None)
        if linefun is not None:
            return linefun()

        self.error(cases.keys())


    def emptyLine(self):
        self.eat(TokenType.SEMICOLON)      

        # move on to next line
        return self.line()


    def returnLine(self):
        # return r = a and b or c + d
        self.eat(TokenType.RETURN)
        
        returnValue = ValueNode(None)
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
        declType = self.type()
        left  = self.identifier(declType.nodeType)
        right = ValueNode(None)

        # type identifier = assignment ;
        if self.current_token.t_type == TokenType.EQUAL:    
            self.eat(TokenType.EQUAL)

            # assigmentLine = assignment ;
            right = self.assignmentLine()
        
        # type identifier (params) block
        elif self.current_token.t_type == TokenType.LEFT_PAREN:
            paramTypes = []
            right = self.function(declType, paramTypes)
            declType = FunctionTypeNode(declType, paramTypes)

        # type identifier ;
        else:
            self.eat(TokenType.SEMICOLON)

        return DeclNode(declType, left, right)


    def function(self, returnType, paramTypes):
        self.eat(TokenType.LEFT_PAREN)
        params = []

        while self.current_token.t_type != TokenType.RIGHT_PAREN and not self.has_error:
            params.append(self.param(paramTypes))

            if self.current_token.t_type != TokenType.RIGHT_PAREN:
                self.eat(TokenType.COMMA)

        self.eat(TokenType.RIGHT_PAREN)
        functionBlock = self.block()

        return FunctionNode(returnType, params, functionBlock)



    def param(self, paramTypes):
        paramType = self.type()
        paramTypes.append(paramType)

        left  = self.identifier(paramType.nodeType)
        right = ValueNode(None)

        # type identifier = assignment
        if self.current_token.t_type == TokenType.EQUAL:    
            self.eat(TokenType.EQUAL)
            right = self.assignment()

# função dentro de parâmetro
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
            n_type = self.compType(left, right, "orExpr")
            _or = BinOpNode(left, right, op, n_type)

        return _or

 
    def andExpr(self):
        _and = self.compExpr()

        while self.current_token.t_type == TokenType.AND:
            left = _and
            op = self.current_token
            self.eat(TokenType.AND)
            right = self.compExpr()
#            print(f"left: {left}, right: {right}")
            n_type = self.compType(left, right, "andExpr")
            _and = BinOpNode(left, right, op, n_type)

        return _and

 
    def compExpr(self):
        _comp = self.expr()

        while self.current_token.t_type in (TokenType.LESS, TokenType.GREATER, TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL, TokenType.EQUAL_EQUAL, TokenType.NOT_EQUAL):
            left = _comp
            op = self.current_token
            self.eat(op.t_type)
            right = self.expr()
            n_type = self.compType(left, right, "compExpr")
            if n_type != NodeType.ERROR:
                n_type = NodeType.BOOL
            _comp = BinOpNode(left, right, op, n_type)

#        print(f"{_comp}")
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
            n_type = self.compType(left, right, "expr")
            _expr = BinOpNode(left, right, op, n_type)

        return _expr


    def term(self):
        _term = self.negation() # ValueNode(10)

        while self.current_token.t_type in (TokenType.STAR, TokenType.SLASH):
            left = _term
            op = self.current_token
            self.eat(op.t_type)
            right = self.negation()
            n_type = self.compType(left, right, "term")
            _term = BinOpNode(left, right, op, n_type)

        return _term

    def compType(self, left, right, exprType):
        if left.nodeType == right.nodeType:
            return left.nodeType
        # "Incompatible Type" was not as helpful
        # to distinguish between syntax and semantics errors
        if NodeType.ERROR not in (left.nodeType, right.nodeType):
            self.error([left.nodeType], f"Invalid Semantics on {exprType}", right)

        return NodeType.ERROR


    def negation(self):
        _negation = None
        if self.current_token.t_type in (TokenType.NOT, TokenType.MINUS):
            op = self.current_token
            self.eat(op.t_type)
            value = self.negation()

            _negation = NegationNode(op, value, value.nodeType)
        else:
            _negation = self.function_call()
        
        return _negation

    def function_call(self):
        _function_call = self.factor()
        if self.current_token == TokenType.LEFT_PAREN:
            self.eat(TokenType.LEFT_PAREN)
            params = []
            while self.current_token.t_type != TokenType.RIGHT_PAREN and not self.has_error:
                params.append(self.assignment())

            if self.current_token.t_type != TokenType.RIGHT_PAREN:
                self.eat(TokenType.COMMA)

            self.eat(TokenType.RIGHT_PAREN)

        return _function_call


    def factor(self):
        _factor = None
        token = self.current_token

        if token.t_type == TokenType.LEFT_PAREN:
            self.eat(TokenType.LEFT_PAREN)
            _factor = self.assignment()
            self.eat(TokenType.RIGHT_PAREN)

        elif token.t_type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            # lookup type on symbol table
            symbol = self.symbolTable.lookup(token.name, None)
            nodeType = None
            if symbol is None:
                self.error([token.name], "Invalid Semantics", "no symbol")
            elif symbol.s_type is None:
                    self.error([token.name], "Invalid Semantics", "undeclared")
            else:
                nodeType = symbol.s_type

            _factor = ValueNode(token, token.name, nodeType)

        elif token.t_type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            _factor = ValueNode(token, token.name, NodeType.NUMBER)

        elif token.t_type == TokenType.STRING:
            self.eat(TokenType.STRING)
            _factor = ValueNode(token, token.name, NodeType.STRING)

        elif token.t_type == TokenType.FALSE:
            self.eat(TokenType.FALSE)
            _factor = ValueNode(token, False, NodeType.BOOL)

        elif token.t_type == TokenType.NULL:
            self.eat(TokenType.NULL)
            _factor = ValueNode(token, None, NodeType.OBJECT)
        
        elif token.t_type == TokenType.TRUE:
            self.eat(TokenType.TRUE)
            _factor = ValueNode(token, True, NodeType.BOOL)

        else:
#            _factor = ErrorNode(token)
            expected = [
                    TokenType.LEFT_PAREN,
                    TokenType.IDENTIFIER,
                    TokenType.NUMBER,
                    TokenType.STRING,
                    TokenType.FALSE,
                    TokenType.NULL,
                    TokenType.TRUE,
            ]
            self.error(expected)

        return _factor

    def nodeTypeFromToken(self, token):
        cases = {
           "Bool": NodeType.BOOL, 
           "Number": NodeType.NUMBER, 
           "String": NodeType.STRING, 
        }

        return cases.get(token.name, NodeType.OBJECT)

    
    def type(self):
        token = self.current_token
        self.eat(TokenType.TYPE)

        nodeType = self.nodeTypeFromToken(token)

        return ValueNode(token, token.name, nodeType)


    def identifier(self, nodeType):
        token = self.current_token
        self.eat(TokenType.IDENTIFIER)

        # not possible, as it's always called from 
        # declaration() or param()
#        declared = nodeType is not None

        _identifier = ValueNode(token, token.name, nodeType) 
 
        # get nodeType from symbolTable
        symbol = self.symbolTable.lookup(token.name, None)
        if symbol is None:
            self.error([nodeType], "Symbol not found", None)
        else: 
            symbol.s_type = nodeType
            symbol.declared = True
            self.symbolTable.insert(token.name, symbol)

        return _identifier 


    def value(self):
        pass
        

    def error(self, types, errMsg="Invalid Syntax", nodeType=None):
        if not self.has_error:
             token = self.current_token

             msg = f"Line {token.line}, {errMsg}: expected "
             # more than one expected option
             if len(types) > 1:
                 msg += "one of "
                 for t in types:
                     msg += f"{str(t)}, "
             else:
                 msg += f"{str(types[0])}, "

             currentType = token.t_type
             if nodeType is not None:
                 currentType = nodeType
                 self.has_semantic_error = True
             # only change current_token, 
             # and report error on syntax errors
             else:
                 self.current_token = Token(token.line, "ERROR", TokenType.ERROR)
                 self.has_error = True


             msg += f"got {currentType}"

             print(msg, file=sys.stderr)



    def eat(self, token_type):
        current_type = self.current_token.t_type
        if current_type == token_type:
#            print(self.current_token)
            if self.lexer.has_next_token() and not self.has_error:
                self.current_token = self.lexer.get_token()
#            # not EOF, as it's always the Lexer's last token
#            else:
#                current_line = self.current_token.line
#                self.current_token = Token(current_line, "ERROR", TokenType.ERROR)
        else:
            self.error([token_type])


"""
Danilo Bizarria
Kaike Rodrigues
Markel Duarte
Matheus Ferreira
Rafael Lino
"""

from enum import Enum, auto


class NodeType(Enum):
    BOOL = auto()
    NUMBER = auto()
    STRING = auto()
    FUNCTION = auto()
    OBJECT = auto()
    ERROR = auto()


class BinOpNode():
    def __init__(self, left, right, op, nodeType = None):
        self.left = left
        self.right = right
        self.op = op
        self.nodeType = nodeType

    def __str__(self):
        return f"({str(self.left)} {self.op.name} {str(self.right)})"

    def accept(self, visitor):
        return visitor.visit_bin_op(self)


class BlockNode():
    def __init__(self, lines):
        self.lines = lines

    def __str__(self):
        return_string = "{\n"
        for line in self.lines:
            return_string += f"{str(line)},\n"
        return_string += "}"

        return return_string

    def accept(self, visitor):
        return visitor.visit_block(self)


class DeclNode():
# Int a = 10;
# DeclNode(Int, a, 10) 

    def __init__(self, typeNode, left, right):
        self.typeNode = typeNode
        self.left = left
        self.right = right

    def __str__(self):
        return f"({str(self.typeNode)} {str(self.left)} = {str(self.right)})"

    def accept(self, visitor):
        return visitor.visit_decl(self)


class ErrorNode():
    def __init__(self, token, msg = "ERROR"):
        self.token = token
        self.msg = msg

    def __str__(self):
        return self.msg

    def accept(self, visitor):
        return visitor.visit_error(self)


class ForNode():
#    precisaria de array
#    for (Fruta fruta in fruteira) { }

    # for (Number i = 0; i < 10; i = i + 1) { }
    def __init__(self, decl, condition, assign, block):
        self.decl = decl
        self.condition = condition
        self.assign = assign
        self.block = block

    def __str__(self):
        return f"(for ({str(self.decl)}; {str(self.condition)}; {str(self.assign)}) {str(self.block)})"

    def accept(self, visitor):
        return visitor.visit_for(self)


class FunctionNode():
    def __init__(self, returnType, params, block):
        self.returnType = returnType
        self.params = params
        self.block = block
        self.arity = len(params)

    def __str__(self):
        fnstr = "("
        for i, param in enumerate(self.params):
            fnstr += f"{str(param)}"
            if i < self.arity - 1:
                fnstr += ", "

        fnstr += f") -> {str(self.returnType)} {str(self.block)}"

        return fnstr

    def accept(self, visitor):
        return visitor.visit_function(self)


class FunctionTypeNode():
    def __init__(self, returnType, paramTypes):
        self.returnType = returnType
        self.paramTypes = paramTypes
        self.nparams = len(paramTypes)

    def __str__(self):
        strType = "(("
        for i, paramType in enumerate(self.paramTypes):
            strType += str(paramType)
            if i < self.nparams - 1:
                strType += ", "

        strType += f") -> {str(self.returnType)})"

        return strType

    def accept(self, visitor):
        return visitor.visit_function_type(self)


class IfNode():
    def __init__(self, condition, ifBlock, elseBlock):
        self.condition = condition
        self.ifBlock = ifBlock
        self.elseBlock = elseBlock


    def __str__(self):
        str_if = f"(if ({str(self.condition)}) {self.ifBlock}"
        if self.elseBlock is not None:
            str_if += f" else {self.elseBlock}"
        
        str_if += ")"
        return str_if


    def accept(self, visitor):
        return visitor.visit_if(self)


class NegationNode():
    def __init__(self, op, value, nodeType):
        self.op = op
        self.value = value
        self.nodeType = nodeType

    def __str__(self):
        return f"({self.op.name} {str(self.value)})" 

    def accept(self, visitor):
        return visitor.visit_negation(self)


class ReturnNode():
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"(return {str(self.value)})"

    def accept(self, visitor):
        return visitor.visit_return(self)


class ValueNode():
    def __init__(self, token, value = None, nodeType = None):
        self.token = token
        self.value = value
        self.nodeType = nodeType

    def __str__(self):
        str_vals = {
                None: "null", 
                False: "false",
                True: "true",
        }
        
        return str_vals.get(self.value, str(self.value))

    def accept(self, visitor):
        return visitor.visit_value(self)


class WhileNode():
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

    def __str__(self):
        return f'(while ({str(self.condition)}) {str(self.block)})'

    def accept(self, visitor):
        return visitor.visit_while(self)


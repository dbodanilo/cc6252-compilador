class IfNode():
    def __init__(self, condition, ifBlock, elseBlock):
        self.condition = condition
        self.ifBlock = ifBlock
        self.elseBlock = elseBlock

    def __str__(self):
        return f'(if ({str(self.condition)}) {self.ifBlock} else {self.elseBlock})'


class BlockNode():
    def __init__(self, lines):
        self.lines = lines

    def __str__(self):
        return_string = "{\n"
        for line in self.lines:
            return_string += f"{str(line)},\n"
        return_string += "}"

        return return_string


class ValueNode():
    def __init__(self, token, value = None):
        self.token = token
        self.value = value

    def __str__(self):
        return str(self.value)


class BinOpNode():
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op

    def __str__(self):
        return f"({str(self.left)} {self.op.name} {str(self.right)})"


class DeclNode():
# Int a = 10;
# DeclNode(Int, a, 10) 

    def __init__(self, type_token, left, right):
        self.type_token = type_token
        self.left = left
        self.right = right

    def __str__(self):
        type_str = ""
        # for function declarations
        if isinstance(self.type_token, list):
            type_str = "["
            for _type in self.type_token:
                type_str += f"{_type.name}, "
            type_str += "]"
        else:
            type_str = self.type_token.name

        return f"({type_str} {self.left.name} = {str(self.right)})"


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


class FunctionNode():
    def __init__(self, params, block):
        self.params = params
        self.block = block

    def __str__(self):
        fnstr = "("
        for param in self.params:
            fnstr += f"{str(param)}, "
        fnstr += f") {str(self.block)}"

        return fnstr


class ReturnNode():
    def __init__(self, value = None):
        self.value = value

    def __str__(self):
        return f"(return {str(self.value)})"


class WhileNode():
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

    def __str__(self):
        return f'(while ({str(self.condition)}) {str(self.block)})'


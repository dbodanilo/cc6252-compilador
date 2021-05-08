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
        return f"({self.type_token.name} {self.left.name} = {str(self.right)})"



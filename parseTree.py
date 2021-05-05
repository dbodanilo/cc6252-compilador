
class ValueNode():
    def __init__(self, token):
        self.token = token
        self.value = token.name

    def __str__(self):
        return self.value


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
        return f"{str(self.left)} = {str(self.right)}"



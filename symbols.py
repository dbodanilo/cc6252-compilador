"""
Token - Linha do codigo, lexema, tokenType

"""

##classe token


class symbol():
    def __init__(self, token, typ, scope):
        self.token = token
        self.typ = typ
        self.scope = scope

class symbolTable():
    def __init__(self):
        self.table = {}

    def insert(self, sym, name):
        table[name] = sym

        return sym

    def lookup(self, name):
        return table[name]

        


##X = symbol(TOK, int, global)



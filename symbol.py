"""
Danilo Bizarria
Kaike Rodrigues
Markel Duarte
Matheus Ferreira
Rafael Lino
"""

"""
{
int a = 10;
}

Token tk_a = Token("a", TokenType.IDENTIFIER, ...)
Symbol(tk_a, LangType.Int, ScopeType.Local)

LangType.Int
scope = local|global

Token - Linha do codigo, lexema, tokenType

X = symbol(TOK, int, global)

"""


from tekken import Token


class Symbol():
    def __init__(self, token, s_type = None, scope = None, declared = False, initialized = False):
        self.token = token
        self.s_type = s_type
        self.scope = scope
        self.declared = declared
        self.initialized = initialized

    def __str__(self):
        str_symbol = f'Token: {str(self.token)}'
        return str_symbol


class SymbolTable():
    def __init__(self):
        # initialize table itself
        self.table = {}


    def insert(self, name, sym):
        self.table[name] = sym

        return sym


    def lookup(self, name):
        return self.table[name]

    def __str__(self):
        str_table = []
        for name in self.table:
            str_table.append(f'{name}: {str(self.table[name])}')
        return str(str_table)


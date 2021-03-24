'''
{
int a = 10;
}

Token tk_a = Token("a", TokenType.IDENTIFIER, ...)
Symbol(tk_a, LangType.Int, ScopeType.Local)

LangType.Int
scope = local|global

Token - Linha do codigo, lexema, tokenType

X = symbol(TOK, int, global)

'''


from token import Token


class Symbol():
    def __init__(self, token, s_type, scope, declared, initialized):
        self.token = token
        self.s_type = s_type
        self.scope = scope
        self.declared = declared
        self.initialized = initialized


class SymbolTable():
    def __init__(self):
        # initialize table itself
        self.table = {}


    def insert(self, sym, name):
        table[name] = sym

        return sym


    def lookup(self, name):
        return table[name]


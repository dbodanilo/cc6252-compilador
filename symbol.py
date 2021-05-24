"""
Danilo Bizarria
Kaike Rodrigues
Markel Duarte
Matheus Ferreira
Rafael Lino
"""

from tekken import Token


class Symbol():
    def __init__(self, token, s_type = None, declared = False, initialized = False, scope = None):
        self.token = token
        self.s_type = s_type
        self.declared = declared
        self.initialized = initialized
        self.scope = scope

    def __str__(self):
        str_symbol = "{\n"
        str_symbol += f"token:  {str(self.token)},\n"
        str_symbol += f"s_type: {str(self.s_type)},\n"
        str_symbol += f"declared {str(self.declared)},\n"
        str_symbol += "}"

        return str_symbol


class SymbolTable():
    def __init__(self):
        # initialize table itself
        self.table = {}


    def insert(self, name, sym):
        self.table[name] = sym

        return sym


    def lookup(self, name, default = None):
        return self.table.get(name, default)


    def __str__(self):
        str_table = "{\n"
        for name in self.table:
            str_table += f"\"{name}\": {str(self.table[name])},\n"
        str_table += "}"
        return str_table


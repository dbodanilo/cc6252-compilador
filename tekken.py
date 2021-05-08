"""
Danilo Bizarria
Kaike Rodrigues
Markel Duarte
Matheus Ferreira
Rafael Lino
"""


from enum import Enum, auto


class TokenType(Enum):
    # one character
    # (
    LEFT_PAREN = auto()
    # )
    RIGHT_PAREN = auto()
    # {
    LEFT_BRACE = auto()
    # }
    RIGHT_BRACE = auto()
    # ,
    COMMA = auto()
    # .
    DOT = auto()
    # -
    MINUS = auto()
    # +
    PLUS = auto()
    # ;
    SEMICOLON = auto()
    # /
    SLASH = auto()
    # *
    STAR = auto()
    # ?
    QUESTION = auto()
    # :
    COLON = auto()
    # =
    EQUAL = auto()
    # >
    GREATER = auto()
    # <
    LESS = auto()

    # two characters
    # /=
    NOT_EQUAL = auto()
    # ==
    EQUAL_EQUAL = auto()
    # >=
    GREATER_EQUAL = auto()
    # <=
    LESS_EQUAL = auto()

    # regexes
#    # \{ [^,]+ (, [^,]+ )* \}
#    ARRAY
    # [a-z][a-zA-Z0-9_]*
    IDENTIFIER = auto()
    # ".*"
    STRING = auto()
    # [+-]?[0-9]+(\.[0-9]+)?
    NUMBER = auto()
    # [A-Z][a-zA-Z0-9_]*
    TYPE = auto()

    # keywords
    # and
    AND = auto()
    # break
    BREAK = auto()
    # continue
    CONTINUE = auto()
    # else
    ELSE = auto()
    # for
    FOR = auto()
    # if
    IF = auto()
    # in
    IN = auto()
    # not
    NOT = auto()
    # or
    OR = auto()
    # return
    RETURN = auto()
    # while
    WHILE = auto()

    # built-in
    # false
    FALSE = auto()
    # null
    NULL = auto()
    # true
    TRUE = auto()

    EOF = auto()
    ERROR = auto()


class Token():
    def __init__(self, line, name, t_type):
        self.line = line
        self.name = name
        self.t_type = t_type
    
    def __str__(self):
        str_token = f"(line {self.line}, \"{self.name}\", {self.t_type})"
        return str_token



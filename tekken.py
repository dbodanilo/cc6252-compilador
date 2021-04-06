"""
Danilo Bizarria
Kaike Rodrigues
Markel Duarte
Matheus Ferreira
Rafael Lino
"""


from enum import Enum


class TokenType(Enum):
    # one character
    # (
    LEFT_PAREN = 1
    # )
    RIGHT_PAREN = 2
    # {
    LEFT_BRACE = 3
    # }
    RIGHT_BRACE = 4
    # ,
    COMMA = 5
    # .
    DOT = 6
    # -
    MINUS = 7
    # +
    PLUS = 8
    # ;
    SEMICOLON = 9
    # /
    SLASH = 10
    # *
    STAR = 11
    # ?
    QUESTION = 12
    # :
    COLON = 13
    # =
    EQUAL = 14
    # >
    GREATER = 15
    # <
    LESS = 16

    # two characters
    # /=
    NOT_EQUAL = 17
    # ==
    EQUAL_EQUAL = 18
    # >=
    GREATER_EQUAL = 19
    # <=
    LESS_EQUAL = 20

    # regexes
    # [a-z][a-zA-Z0-9_]*
    IDENTIFIER = 21
    # ".*"
    STRING = 22
    # [+-]?[0-9]+(\.[0-9]+)?
    NUMBER = 23
    # [A-Z][a-zA-Z0-9_]*
    TYPE = 24

    # keywords
    # and
    AND = 25
    # break
    BREAK = 26
    # continue
    CONTINUE = 27
    # else
    ELSE = 28
    # for
    FOR = 29
    # if
    IF = 30
    # not
    NOT = 31
    # or
    OR = 32
    # return
    RETURN = 33
    # while
    WHILE = 34

    # built-in
    # false
    FALSE = 35
    # null
    NULL = 36
    # true
    TRUE = 37


class Token():
    def __init__(self, line, name, t_type):
        self.line = line
        self.name = name
        self.t_type = t_type


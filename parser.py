from tekken import TokenType


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_token()

    def parse(self):
        return self.line()

    def line(self):
        cases = {
                (TokenType.TYPE: self.declaration,
                TokenType.IDENTIFIER: self.assignmentline,
                TokenType.IF: self.conditional,
                TokenType.FOR: self.loopfor,
                TokenType.WHILE: self.loopwhile
                }

    def declaration():
        continue

    def error(self):
        continue

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_token()
        else:
            self.error()





class PythonGenerator():
    def __init__(self):
        self.level = 0
        

    # only at the beginning of lines
    def print_level(self):
        for i in range(0, self.level):
            print("    ", end="")


    def visit_bin_op(self, node):
        


    def visit_block(self, node):
        for line in node.lines:
            self.print_level()
            line.accept(self)


    def visit_while(self, node):
        self.print_level()
        print("while (", end="")
        self.condition.accept(self)
        print("):")
        self.level += 1
        
        self.block.accept(self) 


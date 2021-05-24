"""
Danilo Bizarria
Kaike Rodrigues
Markel Duarte
Matheus Ferreira
Rafael Lino
"""

from visitor import Visitor


class TreePrinter(Visitor):
    def __init__(self):
        self.level = 0
        self.is_last = False


    def print_level(self):
        for i in range (0, self.level):
            print("  ", end="")


    def print_start(self, msg = "", str_end=":\n"):
        self.print_level()
        print(f"({msg}", end=str_end)
        self.level += 1


    def print_end(self):
        self.level -= 1
        print(")", end="")
        
#        if print_level:
#and "\n" not in str_end:
#            self.print_level()

#        if self.is_last or print_level:
#            str_end = "\n"



    def visit_bin_op(self, node):
        self.print_start(f"BinOp {node.op.name}")
        
        node.left.accept(self)
        print()
        node.right.accept(self)
        
        self.print_end()

        
    def visit_block(self, node):
        self.print_start("Block", str_end=":")
        
        nlines = len(node.lines)
        print_level = nlines > 0
        for i, line in enumerate(node.lines):
            print()
            line.accept(self)
#            # spacing line on all but the last
#            if i < nlines - 1:
#                print()

#        if print_level:
#            print()

        self.print_end()
        

    def visit_decl(self, node):
        self.print_start("Decl")
    
        node.typeNode.accept(self)
        print()
        node.left.accept(self)
        print()
        node.right.accept(self)

        self.print_end()


    def visit_error(self, node):
        self.print_start(f"Error, {node.msg} at {node.token.name}", str_end="")
        self.print_end()

        
    def visit_for(self, node):
        self.print_start("For")

        node.decl.accept(self)
        print()
        node.condition.accept(self)
        print()
        node.assign.accept(self)
        print()
        node.block.accept(self)

        self.print_end()


    def visit_function(self, node):
        self.print_start("Function", str_end=":")

        for param in node.params:
            print()
            param.accept(self)

        print()
        node.block.accept(self)

        self.print_end()


    def visit_function_type(self, node):
        self.print_start("FunctionType")

        node.returnType.accept(self)

        for param in node.paramTypes:
            print()
            param.accept(self)

        self.print_end()


    def visit_if(self, node):
        self.print_start("If")

        node.condition.accept(self)
        print()
        node.ifBlock.accept(self)

        self.print_end()

        if node.elseBlock is not None:
            print()
            self.print_start("Else")
            node.elseBlock.accept(self)
            self.print_end()

#        print()


    def visit_negation(self, node):
        self.print_start("Negation {node.op.name}")

        node.value.accept(self)

        self.print_end()


    def visit_return(self, node):
        self.print_start("Return")

        node.value.accept(self)

        self.print_end()


    def visit_value(self, node):
        self.print_start(str(node), str_end="")
        self.print_end()


    def visit_while(self, node):
        self.print_start("While")

        node.condition.accept(self)
        print()
        node.block.accept(self)

        self.print_end()


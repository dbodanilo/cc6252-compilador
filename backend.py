"""
Danilo Bizarria
Kaike Rodrigues
Markel Duarte
Matheus Ferreira
Rafael Lino
"""

from parseTree import *


class PythonGenerator():
    def __init__(self):
        self.level = 0

 
    def generate(self, node):
        return node.accept(self)
        

    # only at the beginning of lines
    def print_level(self):
        for i in range(0, self.level):
            print("    ", end="")


    def visit_bin_op(self, node):
        node.left.accept(self)

        op_name = node.op.name
        # neq operator distinct from python
        if op_name == "/=":
            op_name = "!="
        print(f" {op_name} ", end="")

        node.right.accept(self) 


    def visit_block(self, node):
        # line = assignment 
        #      | conditional
        #      | declaration
        #      | loopFor
        #      | loopWhile
        #      | returnLine
        for line in node.lines:
            self.print_level()
            line.accept(self)
            print()


    def visit_decl(self, node):
        if node.right.nodeType == NodeType.FUNCTION:
            print("def ", end="")
        node.left.accept(self)
        if node.right.nodeType != NodeType.FUNCTION:
            print(f" = ", end="")
        node.right.accept(self)

    
    def visit_error(self, node):
        print(f"# error: {node.msg} at {node.token.name}")


    def visit_for(self, node):
        # for(...) { } -- empty block
        # not possible in python
        if node.block is not None and len(node.block.lines) > 0: 
            node.decl.accept(self)
            print()
            
            fakeWhile = WhileNode(node.condition, node.block)
            self.visit_while(fakeWhile) 
            
            self.level += 1
            self.print_level()
            node.assign.accept(self)
            self.level -= 1

    
    def visit_function(self, node):
        print("(", end="")
        for i in range(0, node.arity):
            param = node.params[i]
            param.accept(self)
            if i < node.arity - 1:
                print(", ", end="")
        print("):")
        self.level += 1
        node.block.accept(self)
        self.level -= 1


    def visit_function_call(self, node):
        node.name.accept(self)
        print("(", end="")
        arity = len(node.params)
        for i, param in enumerate(node.params):
            param.accept(self)
            if i < arity - 1:
                print(",", end="")
        print(")", end="")


    # probably won't be used
    # as python is not typed
    def visit_function_type(self, node):
        print("# function type")


    def visit_if(self, node):
        # might be an issue for Python:
        # if (cond) {
        #   -- empty
        #} 

        if node.ifBlock is not None and len(node.ifBlock.lines) > 0:
            print("if (", end="")
            node.condition.accept(self)
            print("):")

            self.level += 1        
            node.ifBlock.accept(self)
            self.level -= 1

            if node.elseBlock is not None and len(node.elseBlock.lines) > 0:
                print("\nelse:")

                self.level += 1
                # empty elseBlock an issue as well
                node.elseBlock.accept(self)
                self.level -= 1


    def visit_negation(self, node):
        print(node.op.name, end="")
        
        # print "not x", but "-10"
        if len(node.op.name) > 1:
            print(" ", end="") 
  
        node.value.accept(self)


    def visit_return(self, node):
        print("return ", end="")
        
        node.value.accept(self)


    def visit_value(self, node):
        print(node.value, end="")


    def visit_while(self, node):
        # while(condition) { } 
        # not possible in python
        if node.block is not None and len(node.block.lines) > 0:
            print("while (", end="")
            node.condition.accept(self)
            print("):")

            self.level += 1
            node.block.accept(self) 
            self.level -= 1


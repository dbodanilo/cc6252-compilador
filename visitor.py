from abc import ABC, abstractmethod


class Visitor(ABC):
    @abstractmethod
    def visit_bin_op(self, node):
        pass 


    @abstractmethod
    def visit_block(self, node):
        pass
        

    @abstractmethod
    def visit_decl(self, node):
        pass

        
    @abstractmethod
    def visit_error(self, node):
        pass
        
        
    @abstractmethod
    def visit_for(self, node):
        pass
        
        
    @abstractmethod
    def visit_function(self, node):
        pass
        
        
    @abstractmethod
    def visit_function_type(self, node):
        pass 


    @abstractmethod
    def visit_if(self, node):
        pass

        
    @abstractmethod
    def visit_negation(self, node):
        pass

        
    @abstractmethod
    def visit_return(self, node):
        pass

        
    @abstractmethod
    def visit_value(self, node):
        pass
        

    @abstractmethod
    def visit_while(self, node):
        pass


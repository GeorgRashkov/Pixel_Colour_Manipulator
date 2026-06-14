

class Formula_validation_collections:

    def __init__(self, 
                 allowed_variable_collection_chars:list[str], allowed_variable_chars:list[str],
                 allowed_operator_chars:list[str]=None, allowed_num_chars:list[str]=None, 
                 allowed_special_formulas:list[str]=None):

        self.letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        self.numbers = ['0','1','2','3','4','5','6','7','8','9']

        self.allowed_special_chars = ['.','(',')', '[', ']']
        self.allowed_variable_collection_chars = allowed_variable_collection_chars
        self.allowed_variable_chars = self.allowed_variable_collection_chars + allowed_variable_chars
        self.allowed_operator_chars = ['+','-','*','/','^','%','<','>','='] if allowed_operator_chars == None else allowed_operator_chars
        self.allowed_num_chars = ['0','1','2','3','4','5','6','7','8','9'] if allowed_num_chars == None else allowed_num_chars

        self.allowed_chars = self.allowed_special_chars + self.allowed_variable_chars + self.allowed_operator_chars + self.allowed_num_chars

        self.allowed_special_formulas = ["sin(", "cos(", "tan(", "abs(", "exp(", "sqrt("] if allowed_special_formulas == None else allowed_special_formulas


class RGB_formula_validation_collections(Formula_validation_collections):

    def __init__(self):
        super().__init__(allowed_variable_collection_chars = ['v','r','g','b'], allowed_variable_chars = [])

class Draw_formula_validation_collections(Formula_validation_collections):

    def __init__(self):
        super().__init__(allowed_variable_collection_chars = ['v'], allowed_variable_chars = ['x','y','r','g','b'])

class Dynamic_variable_formula_validation_collections(Formula_validation_collections):

    def __init__(self):
        super().__init__(allowed_variable_collection_chars = ['v'], allowed_variable_chars = [])
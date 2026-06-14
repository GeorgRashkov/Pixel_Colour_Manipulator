

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

        self.allowed_special_formulas = ["sin", "cos", "tan", "abs", "exp", "sqrt"] if allowed_special_formulas == None else allowed_special_formulas
    
    
    #<those functions can be called from outside; those functions should only be used on valid formulas 
    
    def update_format(self, formula:str, model_to_add_to_special_formula:str="np.") -> str:
        
        formula = self.update_format_of_operators(formula=formula)
        formula = self.update_format_of_special_formulas(formula=formula, model_to_add_to_special_formula=model_to_add_to_special_formula)
        formula = self.add_default_indexes_for__variable_collection_chars(formula=formula)
        formula = self.update_indexes_in_square_brackets(formula=formula)

        return formula

    
    def update_format_of_operators(self, formula:str,) -> str:

        formula = formula.replace('^','**').replace('=','==').replace('!','!=')
        return formula

    
    def update_format_of_special_formulas(self, formula:str, model_to_add_to_special_formula:str="np.") -> str:
            
            
            special_formulas = self.allowed_special_formulas
            letters = self.letters

            i = 0
            while(i < len(formula)-1):
                
                if(formula[i] in letters and formula[i+1] in letters):
                    
                    for special_formula in special_formulas:
                        if(formula[i:i+len(special_formula)] == special_formula):
                            formula = formula[:i] + model_to_add_to_special_formula + formula[i:]
                            i+=len(special_formula)
                            break
                
                i+=1
            
            return formula
    
    
    def add_default_indexes_for__variable_collection_chars(self, formula: str):
        
        default_index = "[0]"

        if(len(formula) == 1):
            if(formula in self.allowed_variable_collection_chars):
                formula = formula+default_index
            return formula
            

        for variable_collection_char in self.allowed_variable_collection_chars:

            i = 0
            while(True):
                
                i = formula.find(variable_collection_char,i)
                if(i==-1):
                    break

                if(i==0):
                    if(formula[i+1] == ")" or formula[i+1] in self.allowed_operator_chars):
                        formula = formula[0] + default_index + formula[1:]
                
                elif(i==len(formula)-1):
                    if(formula[i-1] in self.allowed_operator_chars):
                        formula = formula + default_index
                
                elif( formula[i-1] in self.allowed_operator_chars and (formula[i+1] == ")" or formula[i+1] in self.allowed_operator_chars)):
                    formula = formula[:i+1] + default_index + formula[i+1:]

                i+=1
        
        return formula


    
    def update_indexes_in_square_brackets(self, formula: str):

        start_index = 0

        while(True):

            openining_bracket_index = formula.find(f"[",start_index)
            if(openining_bracket_index == -1):
                break

            closing_bracket_index = formula.find("]",openining_bracket_index+1)
            if(closing_bracket_index == -1):
                break
            
            collection_char = formula[openining_bracket_index-1]
            current_index_in_brackets = formula[openining_bracket_index+1:closing_bracket_index]
                
            formula = formula[:closing_bracket_index] + f" if {current_index_in_brackets} < len({collection_char}) else 0" + formula[closing_bracket_index:]

            start_index = formula.find("]",closing_bracket_index+1)
        
        return formula

    
    #those functions can be called from outside>


class RGB_formula_validation_collections(Formula_validation_collections):

    def __init__(self):
        super().__init__(allowed_variable_collection_chars = ['v','r','g','b'], allowed_variable_chars = [])

class Draw_formula_validation_collections(Formula_validation_collections):

    def __init__(self):
        super().__init__(allowed_variable_collection_chars = ['v'], allowed_variable_chars = ['x','y','r','g','b'])

class Dynamic_variable_formula_validation_collections(Formula_validation_collections):

    def __init__(self):
        super().__init__(allowed_variable_collection_chars = ['v'], allowed_variable_chars = [])
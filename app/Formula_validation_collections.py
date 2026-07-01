from Bracket_expressions_getter import get_closing_bracket_index

class Formula_validation_collections:

    def __init__(self, 
                 allowed_variable_collection_chars:list[str], allowed_variable_chars:list[str],
                 allowed_operator_chars:list[str]=None, allowed_num_chars:list[str]=None, 
                 allowed_special_formulas:list[str]=None,
                 special_formulas__content_before_formula:dict[str,str]=None, special_formulas__content_after_first_openning_bracket:dict[str,str]=None, special_formulas__content_before_last_closing_bracket:dict[str,str]=None):

        self.letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        self.numbers = ['0','1','2','3','4','5','6','7','8','9']

        self.allowed_special_chars = ['.','(',')', '[', ']']
        self.allowed_variable_collection_chars = allowed_variable_collection_chars
        self.allowed_variable_chars = self.allowed_variable_collection_chars + allowed_variable_chars
        self.allowed_operator_chars = ['+','-','*','/','^','%','<','>','='] if allowed_operator_chars == None else allowed_operator_chars
        self.allowed_num_chars = ['0','1','2','3','4','5','6','7','8','9'] if allowed_num_chars == None else allowed_num_chars

        self.allowed_chars = self.allowed_special_chars + self.allowed_variable_chars + self.allowed_operator_chars + self.allowed_num_chars

        self.allowed_special_formulas = ["sin", "cos", "tan", "abs", "exp", "sqrt", "randint"] if allowed_special_formulas == None else allowed_special_formulas

        self.special_formulas__content_before_formula = {"sin":"np.", "cos":"np.", "tan":"np.", "abs":"np.", "exp":"np.", "sqrt":"np.", "randint":"np.random."} if special_formulas__content_before_formula == None else special_formulas__content_before_formula
        self.special_formulas__content_after_first_openning_bracket = {"randint":"abs("} if special_formulas__content_after_first_openning_bracket == None else special_formulas__content_after_first_openning_bracket
        self.special_formulas__content_before_last_closing_bracket = {"randint":")+1"} if special_formulas__content_before_last_closing_bracket == None else special_formulas__content_before_last_closing_bracket
    
    
    #<those functions can be called from outside; those functions should only be used on valid formulas 
    
    def update_format(self, formula:str) -> str:
        
        formula = self.update_format_of_operators(formula=formula)
        """
        formula = self.update_format_of_special_formulas(formula=formula, model_to_add_to_special_formula=model_to_add_to_special_formula)
        """
        formula = self.update_format_of_special_formulas(formula=formula)
        formula = self.add_default_indexes_for__variable_collection_chars(formula=formula)
        formula = self.update_indexes_in_square_brackets(formula=formula)

        return formula

    
    def update_format_of_operators(self, formula:str,) -> str:

        formula = formula.replace('^','**').replace('=','==').replace('!','!=')
        return formula


    """
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
    """
    def update_format_of_special_formulas(self, formula:str) -> str:

            for special_formula in self.allowed_special_formulas:
                
                index = 0
                while(True):
                    
                    index = formula.find(special_formula, index)
                    if(index == -1):
                        break
                    
                    #make sure the current special formula is found by ignoring the other special formulas which end with the same sring as the name of the current special formula
                    if(index != 0):
                        if(formula[index-1] in self.letters or formula[index-1] in self.numbers):
                            continue
                    
                    special_formula_openning_bracket_index = index + len(special_formula)

                    #insert content before the last closing bracket for the special formulas which demand the insertion
                    if(special_formula in self.special_formulas__content_before_last_closing_bracket):
                        additional_content = self.special_formulas__content_before_last_closing_bracket[special_formula]
                        special_formula_closing_bracket_index = special_formula_openning_bracket_index + get_closing_bracket_index(txt = formula[special_formula_openning_bracket_index:])
                        formula = formula[:special_formula_closing_bracket_index] + additional_content + formula[special_formula_closing_bracket_index:]
                    
                    #insert content after the first openning bracket for the special formulas which demand the insertion
                    if(special_formula in self.special_formulas__content_after_first_openning_bracket):
                        additional_content = self.special_formulas__content_after_first_openning_bracket[special_formula]
                        formula = formula[:special_formula_openning_bracket_index+1] + additional_content + formula[special_formula_openning_bracket_index+1:]
                    
                    #insert content before the name of the special formula for the special formulas which demand the insertion
                    if(special_formula in self.special_formulas__content_before_formula):
                        additional_content = self.special_formulas__content_before_formula[special_formula]
                        formula = formula[:index] + additional_content + formula[index:]
                        special_formula_openning_bracket_index += len(additional_content)
                    
                    index = special_formula_openning_bracket_index                
            
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
                    if(formula[i-1] == "(" or formula[i-1] in self.allowed_operator_chars):
                        formula = formula + default_index
                
                elif( (formula[i-1] == "(" or formula[i-1] in self.allowed_operator_chars) and 
                     (formula[i+1] == ")" or formula[i+1] in self.allowed_operator_chars)):
                    formula = formula[:i+1] + default_index + formula[i+1:]

                i+=1
        
        return formula


    
    def update_indexes_in_square_brackets(self, formula: str):

        start_index = 0

        while(True):

            openining_bracket_index = formula.find(f"[",start_index)
            if(openining_bracket_index == -1):
                break

            closing_bracket_index = formula.find("]",openining_bracket_index)
            
            collection_char = formula[openining_bracket_index-1]
            current_index_in_brackets = formula[openining_bracket_index+1:closing_bracket_index]
                
            formula = formula[:closing_bracket_index] + f" if {current_index_in_brackets} < len({collection_char}) else 0" + formula[closing_bracket_index:]

            start_index = formula.find("]",openining_bracket_index)
        
        return formula

    
    #those functions can be called from outside>


class RGB_formula_validation_collections(Formula_validation_collections):

    def __init__(self):
        super().__init__(allowed_variable_collection_chars = ['v','r','g','b'], allowed_variable_chars = [], allowed_special_formulas=["sin", "cos", "tan", "abs", "exp", "sqrt"])

class Draw_formula_validation_collections(Formula_validation_collections):

    def __init__(self):
        super().__init__(allowed_variable_collection_chars = ['v'], allowed_variable_chars = ['x','y','r','g','b'])

class Dynamic_variable_formula_validation_collections(Formula_validation_collections):

    def __init__(self):
        super().__init__(allowed_variable_collection_chars = ['v'], allowed_variable_chars = [])
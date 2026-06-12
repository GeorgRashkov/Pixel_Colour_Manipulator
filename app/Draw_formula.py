import numpy as np
from Draw_formula_checker import Draw_formula_validation_collections

class Draw_formula():

    #the provided rgb formulas must be in valid format
    def __init__(self, sub_expressions:list[str], main_expression:str):

        sub_expressions = self.fill_sub_expressions_with_expressions(sub_expressions=sub_expressions)
        main_expression = self.fill_expression_with_expressions(expression=main_expression, sub_expressions=sub_expressions)
        main_expression = self.update_format_of_special_formulas(draw_formula = main_expression)

        main_expression = main_expression.replace('^','**').replace('=','==')
        self.draw_function_str = f"lambda x,y,r,g,b: {main_expression}"
        self.draw_function = eval( self.draw_function_str)
    
    def fill_sub_expressions_with_expressions(self, sub_expressions:list[str]):
        
        sub_expressions_len = len(sub_expressions)
        
        for i in range(1, sub_expressions_len):

            current_expression = sub_expressions[i]
            current_expression_sub_expressions = sub_expressions[0:i]
            current_expression = self.fill_expression_with_expressions(expression=current_expression, sub_expressions=current_expression_sub_expressions)
            sub_expressions[i] = current_expression
        
        return sub_expressions
    
    def fill_expression_with_expressions(self, expression:str, sub_expressions:list[str]) -> str:
        
        v_index = 0
        while(v_index != -1):

            v_index = expression.find("v[", v_index)
            closing_square_bracket_index = expression.find("]", v_index)

            if(v_index == -1 or closing_square_bracket_index == -1):
                break

            v_index_content = int(expression[v_index+2:closing_square_bracket_index])
            sub_expression_content = sub_expressions[v_index_content]

            expression = f"{expression[:v_index]} ( {sub_expression_content} ) {expression[closing_square_bracket_index+1:]}"
        
        return expression
    
    def update_format_of_special_formulas(self, draw_formula:str) -> str:
        
        model_to_add = "np."
        draw_formula_validation_collections = Draw_formula_validation_collections()
        special_formulas = draw_formula_validation_collections.allowed_special_formulas
        letters = draw_formula_validation_collections.letters

        i = 0
        while(i < len(draw_formula)-1):
            
            if(draw_formula[i] in letters and draw_formula[i+1] in letters):
                
                for special_formula in special_formulas:
                    if(draw_formula[i:i+len(special_formula)] == special_formula):
                        draw_formula = draw_formula[:i] + model_to_add + draw_formula[i:]
                        i+=len(special_formula)
                        break
            
            i+=1
        
        return draw_formula

                   

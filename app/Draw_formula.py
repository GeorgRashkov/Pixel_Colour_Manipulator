import numpy as np
from Formula_validation_collections import Draw_formula_validation_collections

class Draw_formula():

    #the provided rgb formulas must be in valid format
    def __init__(self, sub_expressions:list[str], main_expression:str):

        sub_expressions = self.fill_sub_expressions_with_expressions(sub_expressions=sub_expressions)
        main_expression = self.fill_expression_with_expressions(expression=main_expression, sub_expressions=sub_expressions)

        draw_formula_validation_collections = Draw_formula_validation_collections()
        main_expression = draw_formula_validation_collections.update_format(formula=main_expression)

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

                   

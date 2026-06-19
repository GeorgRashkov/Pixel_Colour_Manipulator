
from Formula_validation_collections import Draw_formula_validation_collections
from Formula_checker import check_formula_format, does_formula_contain_specific_variables

def check_draw_formula_expressions_format(main_expression:str, sub_expressions:list[str]) -> bool:
    
    draw_formula_validation_collections = Draw_formula_validation_collections()
    does_formula_contain_atleast_one_x_y_value = does_formula_contain_specific_variables(formula=main_expression, variables=["x","y"], formula_validation_collections=draw_formula_validation_collections, find_all=False)
    if(does_formula_contain_atleast_one_x_y_value == False):
        print("error: the main expression must contain at least at least one value for `x` or `y`")
        return False

    sub_expressions_len = len(sub_expressions)

    for i in range(0, sub_expressions_len):
        is_expression_valid = check_formula_format(formula=sub_expressions[i], expression_name = f"sub expression at index {i}", square_brackets_biggest_value = i-1, formula_validation_collections=draw_formula_validation_collections)
        if(is_expression_valid == False):
            return False
    
    is_expression_valid = check_formula_format(formula=main_expression, expression_name="main expression",  square_brackets_biggest_value = sub_expressions_len-1, formula_validation_collections=draw_formula_validation_collections)
    if(is_expression_valid == False):
        return False
    else:
        return True
    
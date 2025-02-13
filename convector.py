from sympy.parsing.latex import parse_latex
from sympy import Eq, symbols

def latex_to_python(latex_expr):
    space_commands = ["\\quad", "\\qquad", "\\,", "\\:", "\\;", "\\!"]
    for cmd in space_commands:
        latex_expr = latex_expr.replace(cmd, "")

    if "=" in latex_expr:
        try:
            left_expr, right_expr = latex_expr.split("=", 1) 
            left_expr = left_expr.strip()
            right_expr = right_expr.strip()
            
            left_sympy = parse_latex(left_expr)
            right_sympy = parse_latex(right_expr)

            return Eq(left_sympy, right_sympy)  
        except Exception as e:
            raise ValueError(f"Ошибка при обработке равенства: {e}")
    else:
        try:
            sympy_expr = parse_latex(latex_expr)
            return sympy_expr 
        except Exception as e:
            raise ValueError(f"Ошибка при преобразовании: {e}")



from sympy.parsing.latex import parse_latex
from sympy import Eq, Limit

def latex_to_python(latex_expr):
    space_commands = ["\\quad", "\\qquad", "\\,", "\\:", "\\;", "\\!"]
    for cmd in space_commands:
        latex_expr = latex_expr.replace(cmd, "")

    # Явно заменяем \operatorname*{lim} на \lim
    latex_expr = latex_expr.replace(r"\operatorname*{lim}", r"\lim")

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

            # Если это предел, создаем объект Limit без 'dir'
            if isinstance(sympy_expr, Limit):
                return Limit(sympy_expr.args[0], sympy_expr.args[1], sympy_expr.args[2])

            return sympy_expr
        except Exception as e:
            raise ValueError(f"Ошибка при преобразовании: {e}")

# Тест
expr1 = r"\operatorname*{lim}_{x\to0}{\frac{\sin(x)}{x}}"  # Предел
expr2 = r"x^2 + y = 4"  # Уравнение
expr3 = r"\frac{a}{b} + c"  # Обычное выражение

print(latex_to_python(expr1))  # Limit(sin(x)/x, x, 0)
print(latex_to_python(expr2))  # Eq(x**2 + y, 4)
print(latex_to_python(expr3))  # a/b + c

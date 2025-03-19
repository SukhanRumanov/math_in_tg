import sympy as sp

def solve_equation(equation: str):
    try:
        if '=' not in equation:
            return "Некорректное уравнение"
        lhs, rhs = map(sp.sympify, equation.split('='))
        solution = sp.solve(lhs - rhs)
        return solution if solution else "Нет решений"
    except Exception as e:
        return f"Ошибка: {e}"

def calculate_integral(expression: str, variable: str):
    try:
        expr = sp.sympify(expression)
        var = sp.symbols(variable)
        solution = sp.integrate(expr, var)
        return solution
    except Exception as e:
        return f"Ошибка: {e}"

def define_integral(expression: str, var: str, lower: str, upper: str):
    try:
        var_sym = sp.symbols(var)
        lower_sym = sp.sympify(lower)
        upper_sym = sp.sympify(upper)
        expr_sym = sp.sympify(expression)
        result = sp.integrate(expr_sym, (var_sym, lower_sym, upper_sym))
        return result
    except Exception as e:
        return f"Ошибка: {e}"

def calculate_derivative(expression: str, variable: str = 'x'):
    try:
        expr = sp.sympify(expression)
        var = sp.symbols(variable)
        derivative = sp.diff(expr, var)
        return derivative
    except Exception as e:
        return f"Ошибка: {e}"

import sympy as sp

def calculate_limit(expression: str):
    try:
        # Проверяем, начинается ли строка с "Limit(" и заканчивается ли на ")"
        if not expression.startswith("Limit(") or not expression.endswith(")"):
            return "Некорректный формат предела"
        
        # Убираем "Limit(" и ")" и разбиваем аргументы
        inner_args = expression[6:-1]  # Убираем "Limit(" и ")"
        
        # Разбиваем аргументы с учетом того, что dir='+' может содержать запятые
        args = []
        current_arg = ""
        in_quotes = False
        for char in inner_args:
            if char == "'" or char == '"':
                in_quotes = not in_quotes  # Переключаем состояние "в кавычках"
            if char == "," and not in_quotes:
                args.append(current_arg.strip())
                current_arg = ""
            else:
                current_arg += char
        if current_arg:
            args.append(current_arg.strip())
        
        # Проверяем количество аргументов
        if len(args) < 3 or len(args) > 4:
            return "Некорректный формат предела"
        
        # Обрабатываем функцию, переменную и точку
        func = sp.sympify(args[0].strip())
        var = sp.symbols(args[1].strip())
        point = sp.sympify(args[2].strip())
        
        # Обрабатываем направление (если есть)
        direction = None
        if len(args) == 4:
            dir_arg = args[3].strip()
            if dir_arg.startswith("dir="):
                direction = dir_arg[4:].strip("'\"")

        # Вычисляем предел
        solution = sp.limit(func, var, point, dir=direction)
        return solution
    except Exception as e:
        return f"Ошибка: {e}"
def calculate_log(expression: str):
    try:
        if expression.startswith("ln(") and expression.endswith(")"):
            inner = expression[3:-1]  # Убираем "ln(" и ")"
            a = inner.strip()
            a_expr = sp.sympify(a)
            return sp.log(a_expr)  # Натуральный логарифм
        
        elif expression.startswith("lg(") and expression.endswith(")"):
            inner = expression[3:-1]  # Убираем "lg(" и ")"
            a = inner.strip()
            a_expr = sp.sympify(a)
            return sp.log(a_expr, 10)  # Логарифм по основанию 10
        
        elif expression.startswith("log(") and expression.endswith(")"):
            inner = expression[4:-1]  # Убираем "log(" и ")"
            args = [arg.strip() for arg in inner.split(",")]  # Разделяем аргументы
            
            if len(args) == 0 or len(args) > 2:
                return "Неверный формат логарифма"
            
            if len(args) == 1:
                a = args[0]
                a_expr = sp.sympify(a)
                return sp.log(a_expr)  # Натуральный логарифм
            
            elif len(args) == 2:
                a, b = args
                a_expr = sp.sympify(a)
                b_expr = sp.sympify(b)
                
                if b_expr == sp.E:
                    return sp.log(a_expr)
                
                return sp.log(a_expr, b_expr)
        
        return "Не логарифм"
    except Exception as e:
        return f"Ошибка: {e}"
    
import sympy as sp

def format_float(value):
    if isinstance(value, (int, float)):
        str_value = f"{value:.10f}"
        integer_part, fractional_part = str_value.split('.')
        
        result_fractional = ""
        for i, char in enumerate(fractional_part):
            if i >= 5 or char == '0':
                break
            result_fractional += char
        
        if result_fractional:
            return f"{integer_part}.{result_fractional}"
        else:
            return integer_part
    
    return value


def split_and_evaluate(expression: str):
    try:
        parsed_expr = sp.simplify(sp.sympify(expression, evaluate=True))
        result = parsed_expr 
        if isinstance(result, (int, float)):
            return format_float(float(result))  
        return format_float(result)
    except Exception as e:
        return f"Ошибка: {e}"


def determine_and_solve(input_str: str):
    try:
        input_str = input_str.strip()

        if input_str.startswith("Limit(") and input_str.endswith(")"):
            return calculate_limit(input_str)

        # Проверяем, является ли строка уравнением (содержит "=" и не является пределом)
        elif '=' in input_str and not input_str.startswith("Limit("):
            return solve_equation(input_str)

        elif input_str.startswith("Integral"):
            inner = input_str[len("Integral("):-1]
            first_comma = inner.find(",")
            if first_comma == -1:
                return 
            expr = inner[:first_comma].strip()
            rest = inner[first_comma + 1:].strip()
            if rest.startswith("(") and rest.endswith(")"):
                limits = rest[1:-1].split(",")
                if len(limits) == 3:
                    var, lower, upper = [x.strip() for x in limits]
                    return define_integral(expr, var, lower, upper)
                else:
                    return "Неверный формат входных данных для определённого интеграла"
            else:
                var = rest.strip()
                return calculate_integral(expr, var)
        elif input_str.startswith(("log(", "ln(", "lg(")):
            return calculate_log(input_str)
        
        elif input_str.startswith("diff"):
            expr = input_str[len("diff("):-1]
            return calculate_derivative(expr)

        else:
            return split_and_evaluate(input_str)
    
    except Exception as e:
        return f"Ошибка: {e}"
    
print(calculate_limit("Limit(sin(x)/x, x, 0, dir='+')"))
print(determine_and_solve("Limit(sin(x)/x, x, 0, dir='+')"))

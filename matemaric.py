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

def define_integral(expression: str, var_tuple: tuple):
    try:
        expr = sp.sympify(expression)
        var = sp.symbols(var_tuple[0])  # Переменная для интеграла
        lower, upper = var_tuple[1], var_tuple[2]  # Нижний и верхний пределы
        solution = sp.integrate(expr, (var, lower, upper))
        return solution
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

def calculate_limit(expression: str):
    try:
        if not expression.startswith("limit"):
            return "Некорректный формат предела"
        args = expression[6:-1].split(",")
        if len(args) != 3:
            return "Некорректный формат предела"
        func = sp.sympify(args[0].strip())
        var = sp.symbols(args[1].strip())
        point = sp.sympify(args[2].strip())
        solution = sp.limit(func, var, point)
        return solution
    except Exception as e:
        return f"Ошибка: {e}"

def determine_and_solve(input_str: str):
    try:
        input_str = input_str.strip()

        # Проверка на уравнение
        if '=' in input_str:
            return solve_equation(input_str)

        # Обработка интегралов
        elif input_str.startswith("Integral"):
            # Убираем "Integral(" и ")" и разделяем по запятой
            inner = input_str[len("Integral("):-1]
            # Разделяем на выражение и кортеж (переменная, нижний, верхний предел)
            args = inner.split(",")
            expr = args[0].strip()
            var_tuple_str = args[1].strip() if len(args) > 1 else ""

            # Если переданы 3 аргумента (для определённого интеграла)
            if len(args) == 3 and var_tuple_str.startswith("(") and var_tuple_str.endswith(")"):
                var_tuple_str = var_tuple_str[1:-1]  # Убираем скобки
                var_tuple = tuple(map(str.strip, var_tuple_str.split(",")))  # Разделяем по запятой и удаляем пробелы
                return define_integral(expr, var_tuple)

            # Для простых интегралов
            elif len(args) == 2:
                return calculate_integral(expr, var_tuple_str.strip())

        # Обработка производных
        elif input_str.startswith("diff"):
            expr = input_str[len("diff("):-1]  # Убираем "diff("
            return calculate_derivative(expr)

        # Обработка пределов
        elif input_str.startswith("limit"):
            return calculate_limit(input_str)

        else:
            return evaluate_expression(input_str)

    except Exception as e:
        return f"Ошибка: {e}"

def evaluate_expression(expression: str):
    try:
        expr = sp.sympify(expression)
        result = sp.simplify(expr)
        return result
    except Exception as e:
        return f"Ошибка: {e}"

# --- ТЕСТЫ ---
test_cases = [
    "x**2 - 4 = 0",  # Решение уравнения
    "2*x + 5 = 7",  # Решение уравнения
    "Integral(sin(x), x)",  # Обычный интеграл от sin(x)
    "Integral(exp(x), x)",  # Обычный интеграл от exp(x)
    "Integral(x**2, (x, 0, 1))",  # Определённый интеграл от x^2 на [0, 1]
    "Integral(1/x, (x, 1, 3))",  # Определённый интеграл от 1/x на [1, 3]
    "diff(x**3)",  # Производная от x^3
    "diff(sin(x))",  # Производная от sin(x)
    "limit(x**2, x, 2)",  # Предел от x^2 при x → 2
    "limit(1/x, x, 0)",  # Предел от 1/x при x → 0
    "log(8, 2)",  # Логарифм 8 по основанию 2
    "(x**2 + 2*x + 1) / (x + 1)"  # Упрощение выражения
]

for case in test_cases:
    result = determine_and_solve(case)
    print(f"{case} -> {result}")

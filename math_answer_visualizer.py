import matplotlib.pyplot as plt
from sympy import latex, sympify, parse_expr
import uuid
import os

def generate_math_image(expression_str: str, answer_str: str, output_dir: str = "image_answer_photo"):
    try:
        expression = parse_expr(expression_str, evaluate=False)
        expr_latex = latex(expression).replace(r'\limits', '')  
        
        answer = sympify(answer_str)
        answer_latex = latex(answer)

        plt.figure(figsize=(8, 2.5))
        plt.text(0.5, 0.5, 
                 f"Пример: ${expr_latex}$\nОтвет: ${answer_latex}$", 
                 fontsize=20, 
                 ha='center', 
                 va='center')
        plt.axis('off')

        os.makedirs(output_dir, exist_ok=True)
        filename = f"math_{uuid.uuid4().hex}.png"
        filepath = os.path.join(output_dir, filename)
        plt.savefig(filepath, bbox_inches='tight', dpi=150)
        plt.close()

        return filepath

    except Exception as e:
        print(f"Ошибка: {e}")
        return None
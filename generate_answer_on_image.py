from matematic import determine_and_solve
from image_answer import generate_math_image

def process_math_expression(mathonsympy):
    try:
        mathematical_example =mathonsympy
        solution = determine_and_solve(mathonsympy)
        print(solution)
        answer_image = generate_math_image(mathematical_example ,solution)
        answer_image = answer_image.replace("\\", '/')
        print(answer_image)
        return answer_image
    except Exception as e:
        print(f"Ошибка в process_math_expression: {str(e)}")
        raise


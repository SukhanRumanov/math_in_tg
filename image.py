from preprocess import preprocess_image
from convector import latex_to_python
from pix2tex.cli import LatexOCR
from PIL import Image
from generate_answer_on_image import process_math_expression

def process_image(image_path):
    try:
        processed_img = preprocess_image(image_path) 
        pil_img = Image.open(processed_img)
        model = LatexOCR()
        latex = model(pil_img)
        python_code = latex_to_python(latex)

        print(latex)
        print(python_code)

        answer = process_math_expression(str(python_code))
        return answer
    except Exception as e:
        print(f"Ошибка в preprocess_image: {str(e)}")
        raise

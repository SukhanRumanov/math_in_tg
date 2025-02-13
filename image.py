from PIL import Image
from pix2tex.cli import LatexOCR
from convector import latex_to_python

def process_image(image_path):
    img = Image.open(image_path)
    model = LatexOCR()
    latex_formula = model(img)
    print(latex_formula)
    x = latex_to_python(latex_formula)
    print(x)
    return x


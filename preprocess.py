import cv2
import numpy as np
import os
from PIL import Image

def correct_perspective(image):
    """ Исправляет перспективу, если изображение снято под углом """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)  # Поиск контуров

    # Находим контуры
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return image  # Если контуров нет, возвращаем оригинал

    # Берем самый большой контур (предполагаем, что это область формулы)
    largest_contour = max(contours, key=cv2.contourArea)
    epsilon = 0.02 * cv2.arcLength(largest_contour, True)
    approx = cv2.approxPolyDP(largest_contour, epsilon, True)

    if len(approx) == 4:  # Если контур похож на четырехугольник, исправляем перспективу
        pts = np.float32([p[0] for p in approx])
        width = max(np.linalg.norm(pts[0] - pts[1]), np.linalg.norm(pts[2] - pts[3]))
        height = max(np.linalg.norm(pts[1] - pts[2]), np.linalg.norm(pts[3] - pts[0]))

        dst = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32)
        M = cv2.getPerspectiveTransform(pts, dst)
        image = cv2.warpPerspective(image, M, (int(width), int(height)))

    return image

def apply_vignette(image):
    """ Добавляет эффект размытия по краям, чтобы сфокусироваться на центре """
    rows, cols = image.shape[:2]
    
    # Создаем маску градиентного затемнения
    X_resultant_kernel = cv2.getGaussianKernel(cols, cols / 3)
    Y_resultant_kernel = cv2.getGaussianKernel(rows, rows / 3)
    
    kernel = Y_resultant_kernel * X_resultant_kernel.T
    mask = 255 * kernel / np.linalg.norm(kernel)
    
    # Применяем затемнение
    blurred_image = cv2.GaussianBlur(image, (21, 21), 0)
    vignette = cv2.addWeighted(image, 0.7, blurred_image, 0.3, 0)
    
    return vignette

def preprocess_image(image_path):
    # Загружаем изображение
    img = cv2.imread(image_path)

    # Исправляем перспективу
    img = correct_perspective(img)

    # Переводим в градации серого
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Выравниваем контраст (CLAHE)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    img = clahe.apply(img)

    img = apply_vignette(img)

    processed_path = "processed_image.png"
    cv2.imwrite(processed_path, img)

    return processed_path


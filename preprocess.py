import cv2
import numpy as np
import os
def apply_vignette(image, output_folder, step_counter):
    rows, cols = image.shape[:2]
    
    X_resultant_kernel = cv2.getGaussianKernel(cols, cols / 3)
    Y_resultant_kernel = cv2.getGaussianKernel(rows, rows / 3)
    kernel = Y_resultant_kernel * X_resultant_kernel.T
    mask = 255 * kernel / np.linalg.norm(kernel)
    
    cv2.imwrite(f"{output_folder}/{step_counter}_vignette_mask.png", mask)
    step_counter += 1
    
    blurred_image = cv2.GaussianBlur(image, (21, 21), 0)
    cv2.imwrite(f"{output_folder}/{step_counter}_blurred_for_vignette.png", blurred_image)
    step_counter += 1
    
    vignette = cv2.addWeighted(image, 0.7, blurred_image, 0.3, 0)
    cv2.imwrite(f"{output_folder}/{step_counter}_vignette_applied.png", vignette)
    step_counter += 1
    
    return vignette, step_counter

def preprocess_image(image_path):
    output_folder = "preprocess"
    step_counter = 1
    
    img = cv2.imread(image_path)
    cv2.imwrite(f"{output_folder}/{step_counter}_original.png", img)
    step_counter += 1
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(f"{output_folder}/{step_counter}_grayscale.png", gray)
    step_counter += 1
    
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe_img = clahe.apply(gray)
    cv2.imwrite(f"{output_folder}/{step_counter}_clahe.png", clahe_img)
    step_counter += 1
    
    final_img, step_counter = apply_vignette(clahe_img, output_folder, step_counter)
    
    processed_path = f"{output_folder}/final_processed.png"
    cv2.imwrite(processed_path, final_img)
    
    return processed_path

preprocess_image("testimage/test.png")
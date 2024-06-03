import os
from PIL import Image
import pytesseract

# Especifica la ruta al ejecutable de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Cambia esta ruta si es necesario

def image_to_text(image_path, output_path):
    """
    Convierte una imagen a texto y guarda el resultado en un archivo .txt.

    :param image_path: Ruta de la imagen.
    :param output_path: Ruta del archivo de salida .txt.
    """
    try:
        # Abre la imagen
        img = Image.open(image_path)

        # Usa pytesseract para extraer texto de la imagen
        text = pytesseract.image_to_string(img)

        # Guarda el texto en un archivo
        with open(output_path, 'w') as file:
            file.write(text)
        print(f"Texto extraído y guardado en {output_path}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Ruta de la imagen de entrada

    # Ejecuta la función
    image_to_text("pruebas.png", "./")

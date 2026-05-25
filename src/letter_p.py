"""Generowanie litery P za pomocą krzywych B-sklejanych.

Ten moduł generuje binarny obraz litery P używając krzywych B-spline.
Obraz jest generowany jako białe tło z czarną literą P.

Algorytm:
    1. Ładowanie punktów kontrolnych z config/letter_p_config.py
    2. Generowanie wektorów węzłów dla obu krzywych
    3. Generowanie krzywych B-spline dla obu konturów
    4. Rysowanie zewnętrznej krzywej (biała)
    5. Rysowanie wewnętrznej krzywej (czarna - tworzy otwór)

"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.letter_p_config import (
    IMAGE_WIDTH, IMAGE_HEIGHT,
    LETTER_WIDTH, LETTER_HEIGHT,
    MARGIN_X, MARGIN_Y,
    CURVE1_CONTROL_POINTS,
    CURVE2_CONTROL_POINTS
)

from src.bspline import (
    generate_bspline_curve,
    draw_bspline_curves
)


def generate_letter_p_binary_image():
    """
    Generuje binarny obraz litery P używając krzywych B-spline.

    Obraz jest generowany jako białe tło z czarną literą P.
    Funkcja tworzy dwie krzywe B-spline:
    - Zewnętrzną krzywą (biała)
    - Wewnętrzną krzywą (czarna - tworzy otwór)

    Parametry:
        - CURVE1_CONTROL_POINTS: punkty kontrolne zewnętrznej krzywej
        - CURVE2_CONTROL_POINTS: punkty kontrolne wewnętrznej krzywej
        - degree: stopień krzywej (domyślnie 2)
        - num_samples: liczba punktów na krzywej (domyślnie 4001)

    Zwraca:
        (image, curve1, curve2, knots1, knots2) (tuple):
            - image (np.ndarray): Obraz litery P (RGB, 0-255)
            - curve1 (list): Punkty zewnętrznej krzywej
            - curve2 (list): Punkty wewnętrznej krzywej
            - knots1 (np.ndarray): Wektor węzłów zewnętrznej krzywej
            - knots2 (np.ndarray): Wektor węzłów wewnętrznej krzywej

    """
    curve1_points = CURVE1_CONTROL_POINTS
    curve2_points = CURVE2_CONTROL_POINTS
    degree = 2
    num_samples = 4001
    curve1, knots1 = generate_bspline_curve(curve1_points, degree, num_samples)
    curve2, knots2 = generate_bspline_curve(curve2_points, degree, num_samples)
    image = draw_bspline_curves(
        curve1, curve2,
        IMAGE_WIDTH, IMAGE_HEIGHT,
        MARGIN_X, MARGIN_Y,
        color=(255, 255, 255)
    )
    return image, curve1, curve2, knots1, knots2


def save_image(image, filename):
    """
    Zapisuje obraz do pliku.

    Parametry:
        image (np.ndarray): Obraz do zapisu (RGB, 0-255).
        filename (str): Ścieżka do pliku wyjściowego.

    Zwraca:
        None

    """
    from PIL import Image
    pil_image = Image.fromarray(image)
    pil_image.save(filename)
    print(f"Obraz zapisany jako: {filename}")


def main():
    """
    Główna funkcja uruchamiająca generowanie litery P.

    Funkcja:
    1. Generuje binarny obraz litery P
    2. Zapisuje obraz do pliku
    3. Wyświetla informacje o rozmiarach

    Zwraca:
        (image, curve1, curve2) (tuple):
            - image (np.ndarray): Obraz litery P
            - curve1 (list): Punkty zewnętrznej krzywej
            - curve2 (list): Punkty wewnętrznej krzywej

    """
    print("Generowanie litery P za pomocą krzywych B-sklejanych...")
    image, curve1, curve2, knots1, knots2 = generate_letter_p_binary_image()
    save_image(image, "output/letter_p_binary.png")
    print("Generowanie zakończone pomyślnie!")
    print(f"Rozmiar litery: {LETTER_WIDTH}x{LETTER_HEIGHT} pikseli")
    print(f"Rozmiar obrazu: {IMAGE_WIDTH}x{IMAGE_HEIGHT} pikseli")
    return image, curve1, curve2


if __name__ == "__main__":
    main()

"""Generowanie animacji litery P za pomocą krzywych B-sklejanych.

Ten moduł tworzy animację deformacji otworu wewnątrz litery P.
Animacja pokazuje, jak otwór wewnętrzny ulega deformacji (morfowaniu)
w kierunku poziomej linii.

Algorytm animacji:
    1. Dla każdej klatki obliczamy parametr `progress = sin(π * t / num_frames)`
    2. Punkty kontrolne drugiego konturu są morfowane na podstawie `progress`
    3. Generowane są krzywe B-spline dla obu konturów
    4. Obraz jest rysowany z białym zewnętrznym konturem i czarnym wewnętrznym

Morfowanie otworu:
    - Lewa strona otworu pozostaje nieruchoma (przykuta do nogi litery)
    - Prawa strona otworu ulega deformacji w kierunku poziomej linii
    - Efekt tworzy wklęsłą parabolę, która ostatecznie przylega do osi poziomej
    - Parametr `morph_factor` kontroluje stopień deformacji:
      - `morph_factor = 0`: wypukły otwór (stan początkowy)
      - `morph_factor = 1`: wklęsłe zamknięcie przylegające do płaskiej linii

"""

import sys
import os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.letter_p_config import (
    IMAGE_WIDTH, IMAGE_HEIGHT,
    LETTER_HEIGHT,
    MARGIN_X, MARGIN_Y,
    CURVE1_CONTROL_POINTS,
    CURVE2_CONTROL_POINTS
)

from src.bspline import (
    generate_bspline_curve,
    draw_bspline_curves
)


def get_morphed_points(morph_factor):
    """
    Morfowanie punktów otworu litery P.

    Funkcja deformuje punkty kontrolne drugiego konturu (otworu) wewnątrz litery P.
    Morfowanie odbywa się w dwóch kierunkach:
    1. Lewa strona otworu pozostaje nieruchoma (przykuta do nogi litery)
    2. Prawa strona otworu ulega deformacji w kierunku poziomej linii

    Parametry:
        morph_factor (float): Parametr interpolacji od 0 do 1.
            - 0: wypukły otwór (stan początkowy)
            - 1: wklęsłe zamknięcie przylegające do płaskiej linii

    Zwraca:
        morphed_points (list): Lista zmodyfikowanych punktów kontrolnych.

    """
    y_mid = -215
    
    p0 = (50, -180)
    p1 = (50, -180)
    p2 = (50, -250)
    p3 = (50, -250)

    p4_x = 150 + (50 - 150) * morph_factor
    p4_y = -250 + (y_mid - (-250)) * morph_factor
    
    p5_x = 150
    p5_y = y_mid
    
    p6_x = 150 + (50 - 150) * morph_factor
    p6_y = -180 + (y_mid - (-180)) * morph_factor
    
    p4 = (p4_x, p4_y)
    p5 = (p5_x, p5_y)
    p6 = (p6_x, p6_y)
    
    p7 = (50, -180)
    p8 = (50, -180)
    
    return [p0, p1, p2, p3, p4, p5, p6, p7, p8]


def create_animation_frames(num_frames=200):
    """
    Tworzy klatki animacji deformacji otworu litery P.

    Funkcja generuje animację pokazującą deformację otworu wewnątrz litery P.
    Dla każdej klatki:
    1. Obliczamy parametr `progress = sin(π * t / num_frames)`
    2. Morfujemy punkty kontrolne drugiego konturu na podstawie `progress`
    3. Generujemy krzywe B-spline dla obu konturów
    4. Rysujemy obraz z białym zewnętrznym konturem i czarnym wewnętrznym

    Parametry:
        num_frames (int): Liczba klatek animacji (domyślnie 200).

    Zwraca:
        frames (list): Lista klatek (numpy arrays RGB).

    """
    frames = []
    
    for t in range(num_frames):
        progress = np.sin(np.pi * t / num_frames)
        
        animated_curve2_points = get_morphed_points(progress)
        
        curve1, _ = generate_bspline_curve(CURVE1_CONTROL_POINTS, 2, 4001)
        curve2, _ = generate_bspline_curve(animated_curve2_points, 2, 4001)
        
        image = draw_bspline_curves(
            curve1, curve2,
            IMAGE_WIDTH, IMAGE_HEIGHT,
            MARGIN_X, MARGIN_Y
        )
        frames.append(image)
    return frames


def save_animation(frames, filename, fps=10):
    """
    Zapisuje animację do pliku wideo.

    Funkcja zapisuje listę klatek do pliku wideo w formacie MP4.

    Parametry:
        frames (list): Lista klatek (numpy arrays RGB).
        filename (str): Ścieżka do pliku wyjściowego (np. `output/letter_p_animation.mp4`).
        fps (int): Klatki na sekundę (domyślnie 10).

    Zwraca:
        filename (str): Ścieżka zapisanego pliku wideo.

    """
    from PIL import Image
    import cv2
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    
    writer = cv2.VideoWriter(filename, fourcc, fps, (IMAGE_WIDTH, IMAGE_HEIGHT))
    
    for frame in frames:
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        writer.write(frame_bgr)
    
    writer.release()
    print(f"Animacja zapisana jako: {filename}")
    
    return filename


def main():
    """
    Główna funkcja uruchamiająca generowanie animacji.

    Funkcja:
    1. Generuje animację litery P
    2. Zapisuje animację do pliku
    3. Wyświetla informacje o liczbie klatek i rozdzielczości

    Zwraca:
        frames (list): Lista klatek animacji.

    """
    print("Generowanie animacji litery P...")
    print(f"Liczba klatek: {200}")
    print(f"Rozdzielczość: {IMAGE_WIDTH}x{IMAGE_HEIGHT}")
    
    frames = create_animation_frames(num_frames=200)
    
    save_animation(frames, "projekt2/output/letter_p_animation.mp4", fps=10)
    
    print("Generowanie animacji zakończone pomyślnie!")
    
    return frames


if __name__ == "__main__":
    main()

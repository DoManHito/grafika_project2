#!/usr/bin/env python3
"""
Uruchamianie generowania litery P i animacji.

Ten skrypt jest głównym punktem wejścia do aplikacji.
Uruchamia generowanie litery P oraz animację deformacji otworu.

Algorytm:
    1. Generowanie litery P:
       - Ładowanie punktów kontrolnych z config/letter_p_config.py
       - Generowanie krzywych B-spline dla obu konturów
       - Rysowanie litery P na obrazie
       - Zapisywanie obrazu do pliku PNG

    2. Generowanie animacji:
       - Morfowanie otworu litery P w czasie
       - Generowanie klatek animacji
       - Zapisywanie animacji do pliku MP4

Uruchomienie:
    python run.py

Generuje:
    - output/letter_p_binary.png - binarny obraz litery P
    - output/letter_p_animation.mp4 - animacja litery P
"""

import sys
import os

# Dodaj katalog projektu do ścieżki
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.letter_p import main as run_letter_p
from src.animation import main as run_animation


def main():
    """
    Główna funkcja uruchamiająca cały projekt.

    Funkcja:
    1. Generuje binarny obraz litery P
    2. Generuje animację deformacji otworu
    3. Wyświetla informacje o zakończeniu procesu

    Zwraca:
        None

    """
    print("=" * 60)
    print("PROJEKT 2: Krzywe B-sklejane w Grafice Komputerowej")
    print("=" * 60)
    print()
    
    # Uruchom generowanie litery P
    print("Część I: Generowanie litery P...")
    print("-" * 40)
    run_letter_p()
    print()
    
    # Uruchom generowanie animacji
    print("Część II: Generowanie animacji...")
    print("-" * 40)
    run_animation()
    print()
    
    print("=" * 60)
    print("PROJEKT ZAKOŃCZONY Pomyślnie!")
    print("=" * 60)
    print()
    print("Wygenerowane pliki:")
    print("  - output/letter_p_binary.png")
    print("  - output/letter_p_animation.mp4")
    print()


if __name__ == "__main__":
    main()

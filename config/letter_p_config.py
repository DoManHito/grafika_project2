"""Konfiguracja kształtu litery P.

Ten plik definiuje parametry geometryczne litery P:
- Rozmiar obrazu i marginesy
- Punkty kontrolne dla zewnętrznej i wewnętrznej krzywej B-spline

Punkty kontrolne są podawane jako lista par (x, y) w układzie współrzędnych
relatywnym do lewego górnego rogu litery. Oś Y rośnie w dół (układ ekranowy).

Dlaczego punkty są duplikowane?
    W krzywych B-spline stopnia k, pierwsze i ostatnie k punktów kontrolnych
    są powtarzane, aby zapewnić interpolację (krzywa przechodzi przez punkty
    kontrolne na początku i końcu). Dla stopnia 2 (kwadratowej krzywej)
    potrzebujemy 2 powtórzenia na początku i końcu.

Układ współrzędnych:
    - (0, 0): lewy górny róg litery
    - Oś X: rośnie w prawo
    - Oś Y: rośnie w dół (jak w obrazach)
    - Marginesy: MARGIN_X i MARGIN_Y są dodawane do współrzędnych krzywej
      przy rysowaniu na obrazie.

"""

# Rozmiar obrazu wyjściowego
IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480

# Rozmiar litery P wewnątrz obrazu
LETTER_WIDTH = 200
LETTER_HEIGHT = 300

# Marginesy - pozycjonowanie litery w obrazie
MARGIN_X = (IMAGE_WIDTH - LETTER_WIDTH) // 2
MARGIN_Y = (IMAGE_HEIGHT - LETTER_HEIGHT) // 2

# Zewnętrzny kontur litery P (CRVE1)
# Punkty kontrolne definiują kształt zewnętrznej krawędzi litery P
# Krzywa przechodzi przez punkty 2, 4, 6, 8, 10, 12 (nieparzyste indeksy)
CURVE1_CONTROL_POINTS = [
    (0, 0),                              # Punkt 0: lewy dolny róg (start)
    (0, 0),                              # Punkt 1: duplikat - stabilizacja dolnego lewego rogu
    (0, -LETTER_HEIGHT),                 # Punkt 2: górny lewy róg (początek łuku)
    (0, -LETTER_HEIGHT),                 # Punkt 3: duplikat - stabilizacja górnego lewego rogu
    (LETTER_WIDTH, -LETTER_HEIGHT),      # Punkt 4: górny prawy róg (koniec łuku)
    (LETTER_WIDTH, -LETTER_HEIGHT + 170),# Punkt 5: dolny prawy róg "uszka"
    (50, -LETTER_HEIGHT + 170),          # Punkt 6: wewnętrzny róg pod "uszkiem"
    (50, -LETTER_HEIGHT + 170),          # Punkt 7: duplikat - stabilizacja wewnętrznego rogu
    (50, 0),                             # Punkt 8: dolny prawy róg nogi
    (50, 0),                             # Punkt 9: duplikat - stabilizacja dolnego prawego rogu
    (0, 0),                              # Punkt 10: powrót do lewego dolnego rogu
    (0, 0)                               # Punkt 11: duplikat - zamknięcie konturu
]

# Wewnętrzny kontur (otwór wewnątrz litery P) (CURVE2)
# Ten kontur definiuje kształt otworu wewnątrz litery P
# W animacji ten otwór ulega deformacji (morfowaniu)
CURVE2_CONTROL_POINTS = [
    (50, -LETTER_HEIGHT + 120),          # Punkt 0: dolny lewy róg otworu (przy nodze)
    (50, -LETTER_HEIGHT + 120),          # Punkt 1: duplikat - stabilizacja dolnego lewego rogu
    (50, -LETTER_HEIGHT + 50),           # Punkt 2: górny lewy róg otworu
    (50, -LETTER_HEIGHT + 50),           # Punkt 3: duplikat - stabilizacja górnego lewego rogu
    (150, -LETTER_HEIGHT + 50),          # Punkt 4: górny prawy róg otworu
    (150, -LETTER_HEIGHT + 120),         # Punkt 5: dolny prawy róg otworu
    (50, -LETTER_HEIGHT + 120),          # Punkt 6: powrót do dolnego lewego rogu
    (50, -LETTER_HEIGHT + 120)           # Punkt 7: duplikat - zamknięcie konturu
]

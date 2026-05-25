# Instrukcja uruchomienia projektu

## Wymagania

- Python 3.7+
- Biblioteki: numpy, matplotlib, opencv-python, scipy, Pillow

## Instalacja

```bash
pip install -r requirements.txt
```

## Uruchomienie

### Opcja 1: Uruchomienie całego projektu

```bash
python run.py
```

### Opcja 2: Uruchomienie poszczególnych części

```bash
# Część I: Generowanie litery P
python src/letter_p.py

# Część II: Generowanie animacji
python src/animation.py
```

## Wyjściowe pliki

Po uruchomieniu projektu w katalogu `output/` pojawią się:

- `letter_p_binary.png` - Binarny obraz litery P (biały tło, czarna litera)
- `letter_p_animation.mp4` - Animacja litery P (200 klatek, 10 fps)

## Opis krzywych B-sklejanych

Krzywa B-sklejana stopnia k jest zdefiniowana jako:

```
B(t) = Σ[i=0..n] N(i,k,u) * P[i]
```

gdzie:
- `N(i,k,u)` - funkcje bazowe B-spline
- `P[i]` - punkty kontrolne
- `u` - parametr krzywej (0 ≤ u ≤ 1)

Funkcje bazowe B-spline stopnia k definiowane rekurencyjnie:

```
N(i,0,u) = 1, jeśli i ≤ u < i+1, inaczej 0
N(i,k,u) = (u - u[i]) / (u[i+k] - u[i]) * N(i,k-1,u) +
           (u[i+k+1] - u) / (u[i+k+1] - u[i+1]) * N(i+1,k-1,u)
```

## Modyfikacja kształtu litery P

Aby zmienić kształt litery P, edytuj plik `config/letter_p_config.py`:

### Punkty kontrolne

1. **`CURVE1_CONTROL_POINTS`** - zewnętrzny kontur litery P:
   - Pierwsze 2 punkty: dolny lewy róg (duplikowane dla stabilizacji)
   - Punkty 3-4: górny lewy róg (duplikowane)
   - Punkty 5-6: górna prawa część (na prowadząca dla łuku)
   - Punkty 7-8: wewnętrzny róg pod "uszkiem" (duplikowane)
   - Punkty 9-10: dolny prawy róg nogi (duplikowane)
   - Punkty 11-12: powrót do początku (duplikowane)

2. **`CURVE2_CONTROL_POINTS`** - wewnętrzny kontur (otwór):
   - Punkty 1-2: dolny lewy róg otworu (duplikowane)
   - Punkty 3-4: górny lewy róg otworu (duplikowane)
   - Punkty 5-6: prawa strona otworu (na prowadząca dla łuku)
   - Punkty 7-8: zamknięcie otworu (duplikowane)

### Rozmiar litery

3. **`LETTER_WIDTH`** i **`LETTER_HEIGHT`** - rozmiar litery w pikselach
   - Obraz jest generowany z marginesem: `MARGIN_X` i `MARGIN_Y`
   - `IMAGE_WIDTH = 640`, `IMAGE_HEIGHT = 480` (domyślne)

## Modyfikacja animacji

Aby zmienić parametry animacji, edytuj plik `src/animation.py`:

### Morfowanie otworu

Funkcja `get_morphed_points(morph_factor)` kontroluje deformację otworu:

- **`morph_factor`**: parametr interpolacji od 0 do 1
  - `morph_factor = 0`: wypukły otwór (stan początkowy)
  - `morph_factor = 1`: wklęsłe zamknięcie przylegające do płaskiej linii

### Tworzenie klatek

Funkcja `create_animation_frames(num_frames)` generuje animację:

1. Dla każdej klatki obliczany jest `progress = sin(π * t / num_frames)`
2. Punkty kontrolne drugiego konturu są morfowane na podstawie `progress`
3. Generowane są krzywe B-spline dla obu konturów
4. Obraz jest rysowany z białym zewnętrznym konturem i czarnym wewnętrznym

### Zapis animacji

Funkcja `save_animation(frames, filename, fps)` zapisuje animację:

- `frames`: lista klatek (numpy arrays RGB)
- `filename`: ścieżka do pliku wyjściowego (np. `output/letter_p_animation.mp4`)
- `fps`: klatki na sekundę (domyślnie 10)
- Używa kodeka `mp4v` do zapisu w formacie MP4

### Parametry do modyfikacji

1. **`num_frames`** - liczba klatek animacji (domyślnie 200)
2. **`fps`** - klatki na sekundę (domyślnie 10)
3. **`y_mid`** - pozioma pozycja do której otwór się deformuje (domyślnie -215)

## Elementy oceny

- **Część 1 (20%)**: Analiza problemu i opis rozwiązania
- **Część 2 (10%)**: Animacja
- **Kody źródłowe (30%)**: Czytelność, brak redundancji
- **Wyniki (40%)**: Poprawność i wizualna atrakcyjność

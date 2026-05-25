# Projekt 2: Krzywe B-sklejane w Grafice Komputerowej

## Opis projektu
Projekt wykorzystuje krzywe B-sklejane (B-spline) do generowania kształtu litery P oraz tworzenia animacji.

## Struktura projektu
```
projekt2/
├── README.md              # Ten plik
├── requirements.txt       # Wymagane zależności
├── config/
│   └── letter_p_config.py # Konfiguracja kształtu litery P
├── src/
│   ├── __init__.py
│   ├── bspline.py        # Moduł krzywych B-spline
│   ├── letter_p.py       # Generowanie litery P
│   └── animation.py      # Generowanie animacji
└── output/
    ├── letter_p_binary.png  # Wynikowy obraz binarny
    └── letter_p_animation.mp4  # Animacja
```

## Instalacja
```bash
pip install -r requirements.txt
```

## Uruchomienie
```bash
python src/letter_p.py
python src/animation.py
```

## Opis krzywych B-sklejanych

Krzywa B-sklejana (B-spline) to krzywa parametryczna zdefiniowana przez:
```
B(t) = Σ[i=0..n] N(i,k,u) * P[i]
```

gdzie:
- `N(i,k,u)` - funkcje bazowe B-spline (Basis Functions)
- `P[i]` - punkty kontrolne (control points)
- `u` - parametr krzywej (0 ≤ u ≤ 1)
- `k` - stopień krzywej (liczba punktów kontrolne minus 1)
- `n` - liczba punktów kontrolnych minus 1

### Funkcje bazowe B-spline

Funkcje bazowe B-spline definiowane są rekurencyjnie (Coxa-de Boor formula):

```
N(i,0,u) = 1, jeśli i ≤ u < i+1, inaczej 0 (stopień 0)
N(i,k,u) = (u - u[i]) / (u[i+k] - u[i]) * N(i,k-1,u) +
           (u[i+k+1] - u) / (u[i+k+1] - u[i+1]) * N(i+1,k-1,u)
```

### Wektor węzłów (Knot Vector)

Wektor węzłów definiuje podział domeny krzywej na segmenty. Dla krzywej B-spline stopnia k z n punktami kontrolnymi:
- Liczba węzłów: `num_knots = n + k + 1`
- Pierwsze k węzłów: `0` (powtarzane)
- Ostatnie k węzłów: `1` (powtarzane)
- Środkowe węzły: równomiernie rozłożone w zakresie `(0, 1)`

### Generowanie krzywej

1. **Generowanie wektora węzłów**: Tworzenie wektora węzłów na podstawie liczby punktów kontrolnych i stopnia krzywej.

2. **Generowanie krzywej**: Dla każdego punktu `u` w zakresie `[0, 1]` obliczamy punkt na krzywej używając funkcji bazowych.

3. **Wyrysowanie krzywej**: Punkty krzywej są transformowane do układu współrzędnych obrazu i wypełniane jako wielokąty.

### Morfowanie otworu w animacji

W animacji otwór wewnętrzny litery P ulega deformacji:
- Lewa strona otworu pozostaje nieruchoma (przykuta do nogi litery)
- Prawa strona otworu ulega deformacji w kierunku poziomej linii
- Efekt tworzy wklęsłą parabolę, która ostatecznie przylega do osi poziomej
- Parametr `morph_factor` kontroluje stopień deformacji:
  - `morph_factor = 0`: wypukły otwór (stan początkowy)
  - `morph_factor = 1`: wklęsłe zamknięcie przylegające do płaskiej linii

## Elementy oceny
- Część 1 (20%): Analiza problemu i opis rozwiązania
- Część 2 (10%): Animacja
- Kody źródłowe (30%)
- Wyniki (40%)

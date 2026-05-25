"""Moduł do generowania krzywych B-sklejanych (B-spline).

Krzywa B-sklejana (B-spline) to krzywa parametryczna zdefiniowana przez:
    B(t) = Σ[i=0..n] N(i,k,u) * P[i]

gdzie:
    - N(i,k,u) - funkcje bazowe B-spline (Basis Functions)
    - P[i] - punkty kontrolne (control points)
    - u - parametr krzywej (0 ≤ u ≤ 1)
    - k - stopień krzywej (liczba punktów kontrolne minus 1)
    - n - liczba punktów kontrolnych minus 1

Funkcje bazowe B-spline definiowane są rekurencyjnie (Coxa-de Boor formula):
    N(i,0,u) = 1, jeśli i ≤ u < i+1, inaczej 0 (stopień 0)
    N(i,k,u) = (u - u[i]) / (u[i+k] - u[i]) * N(i,k-1,u) +
               (u[i+k+1] - u) / (u[i+k+1] - u[i+1]) * N(i+1,k-1,u)

"""

import cv2
import numpy as np


def generate_knot_vector(num_control_points, degree):
    """
    Generuje wektor węzłów (knot vector) dla krzywej B-spline.

    Wektor węzłów definiuje podział domeny krzywej na segmenty.
    Dla krzywej B-spline stopnia k z n punktami kontrolnymi:
        - Liczba węzłów: num_knots = n + k + 1
        - Pierwsze k węzłów: 0 (powtarzane)
        - Ostatnie k węzłów: 1 (powtarzane)
        - Środkowe węzły: równomiernie rozłożone w zakresie (0, 1)

    Parametry:
        num_control_points (int): Liczba punktów kontrolnych krzywej.
        degree (int): Stopień krzywej B-spline (k = degree).
                        Dla krzywej stopnia 2 mamy krzywą kwadratową.

    Zwraca:
        knots (np.ndarray): Wektor węzłów o długości num_control_points + degree + 1.

    Przykład:
        Dla 9 punktów kontrolnych i stopnia 2:
        knots = [0, 0, 0, 0.33, 0.66, 1, 1, 1, 1]

    """
    n = num_control_points
    k = degree
    num_knots = n + k + 1
    knots = np.zeros(num_knots)
    knots[n:] = 1.0
    if n > k + 1:
        knots[k+1:n] = np.linspace(0, 1, n - k + 1)[1:-1]
    return knots


def basis_function(i, degree, u, knots):
    """
    Oblicza funkcję bazową B-spline dla danego indeksu i parametru u.

    Funkcje bazowe B-spline definiowane są rekurencyjnie (Coxa-de Boor formula):
        N(i,0,u) = 1, jeśli i ≤ u < i+1, inaczej 0 (stopień 0)
        N(i,k,u) = (u - u[i]) / (u[i+k] - u[i]) * N(i,k-1,u) +
                   (u[i+k+1] - u) / (u[i+k+1] - u[i+1]) * N(i+1,k-1,u)

    Parametry:
        i (int): Indeks punktu kontrolnego.
        degree (int): Stopień funkcji bazowej.
        u (float): Parametr krzywej (0 ≤ u ≤ 1).
        knots (np.ndarray): Wektor węzłów.

    Zwraca:
        value (float): Wartość funkcji bazowej dla danego indeksu i parametru u.

    """
    if degree == 0:
        # Stopień 0: funkcja bazowa jest 1, jeśli u leży w przedziale [i, i+1)
        if knots[i] <= u < knots[i + 1] or (u == 1.0 and knots[i + 1] == 1.0 and knots[i] < 1.0):
            return 1.0
        return 0.0
    else:
        # Rekurencyjne obliczenie dla wyższych stopni
        denom_left = knots[i + degree] - knots[i]
        if denom_left != 0:
            left = (u - knots[i]) / denom_left * basis_function(i, degree - 1, u, knots)
        else:
            left = 0.0

        denom_right = knots[i + degree + 1] - knots[i + 1]
        if denom_right != 0:
            right = (knots[i + degree + 1] - u) / denom_right * basis_function(i + 1, degree - 1, u, knots)
        else:
            right = 0.0

        return left + right


def evaluate_bspline(points, degree, u, knots=None):
    """
    Oblicza punkt na krzywej B-spline dla danego parametru u.

    Krzywa B-spline jest zdefiniowana jako:
        B(t) = Σ[i=0..n] N(i,k,u) * P[i]

    Parametry:
        points (list): Lista punktów kontrolnych [(x0, y0), (x1, y1), ...].
        degree (int): Stopień krzywej.
        u (float): Parametr krzywej (0 ≤ u ≤ 1).
        knots (np.ndarray, opcjonalne): Wektor węzłów. Jeśli None, zostanie wygenerowany.

    Zwraca:
        (x, y) (tuple): Współrzędne punktu na krzywej dla parametru u.

    """
    if knots is None:
        knots = generate_knot_vector(len(points), degree)
    x = sum(basis_function(i, degree, u, knots) * p[0] for i, p in enumerate(points))
    y = sum(basis_function(i, degree, u, knots) * p[1] for i, p in enumerate(points))
    return x, y


def generate_bspline_curve(points, degree, num_samples=4001):
    """
    Generuje krzywą B-spline dla podanej listy punktów kontrolnych.

    Krzywa jest generowana przez obliczanie punktów dla równomiernie rozłożonych
    wartości parametru u w zakresie [0, 1].

    Parametry:
        points (list): Lista punktów kontrolnych [(x0, y0), (x1, y1), ...].
        degree (int): Stopień krzywej B-spline.
        num_samples (int): Liczba punktów do wygenerowania na krzywej.

    Zwraca:
        (curve, knots) (tuple):
            - curve (list): Lista punktów [(x, y), ...] tworzących krzywą.
            - knots (np.ndarray): Wektor węzłów użyty do generowania krzywej.

    """
    knots = generate_knot_vector(len(points), degree)
    u_values = np.linspace(0, 1, num_samples)
    curve = []
    for u in u_values:
        x, y = evaluate_bspline(points, degree, u, knots)
        curve.append((x, y))
    return curve, knots


def generate_two_bspline_curves(points1, points2, degree=2, num_samples=4001):
    """
    Generuje dwie krzywe B-spline dla podanych list punktów kontrolnych.

    Parametry:
        points1 (list): Lista punktów kontrolnych dla pierwszej krzywej.
        points2 (list): Lista punktów kontrolnych dla drugiej krzywej.
        degree (int): Stopień krzywych (domyślnie 2).
        num_samples (int): Liczba punktów do wygenerowania na każdej krzywej.

    Zwraca:
        (curve1, curve2) (tuple):
            - curve1 (list): Lista punktów pierwszej krzywej.
            - curve2 (list): Lista punktów drugiej krzywej.

    """
    curve1, _ = generate_bspline_curve(points1, degree, num_samples)
    curve2, _ = generate_bspline_curve(points2, degree, num_samples)
    return curve1, curve2


def draw_bspline_curves(curve1, curve2, image_width, image_height, margin_x, margin_y, color=(255, 255, 255)):
    """
    Rysuje dwie krzywe B-spline na obrazie.

    Funkcja transformuje punkty krzywej do układu współrzędnych obrazu,
    wypełnia wielokąty zewnętrzną i wewnętrzną krzywą, a następnie
    rysuje kontury.

    Parametry:
        curve1 (list): Lista punktów pierwszej krzywej [(x, y), ...].
        curve2 (list): Lista punktów drugiej krzywej [(x, y), ...].
        image_width (int): Szerokość obrazu w pikselach.
        image_height (int): Wysokość obrazu w pikselach.
        margin_x (int): Margines poziomy (pozycjonowanie w obrazie).
        margin_y (int): Margines pionowy (pozycjonowanie w obrazie).
        color (tuple): Kolor wypełnienia zewnętrznej krzywej (RGB).

    Zwraca:
        image (np.ndarray): Obraz z narysowanymi krzywymi.

    """
    image = np.zeros((image_height, image_width, 3), dtype=np.uint8)

    def transform_curve(curve):
        pts = []
        for p in curve:
            x = int(margin_x + p[0])
            y = int(margin_y + (image_height - 2 * margin_y) + p[1])
            pts.append([x, y])
        return np.array(pts, dtype=np.int32)

    pts1 = transform_curve(curve1)
    pts2 = transform_curve(curve2)

    cv2.fillPoly(image, [pts1], color)

    cv2.fillPoly(image, [pts2], (0, 0, 0))

    return image
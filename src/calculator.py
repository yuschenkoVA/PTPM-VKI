import math

class TriangleCalculator:

    def compute(self, s1, s2, s3):
        try:
            a, b, c = float(s1), float(s2), float(s3)
        except (ValueError, TypeError):
            return "", "Нечисловые данные"

        if a <= 0 or b <= 0 or c <= 0:
            return "не треугольник", "Стороны должны быть положительными"

        x, y, z = sorted([a, b, c])
        if x + y <= z + 1e-9:
            return "не треугольник", "Сумма двух сторон не больше третьей"

        if math.isclose(a, b, abs_tol=1e-9) and math.isclose(b, c, abs_tol=1e-9):
            return "равносторонний", ""
        elif math.isclose(a, b, abs_tol=1e-9) or math.isclose(b, c, abs_tol=1e-9) or math.isclose(a, c, abs_tol=1e-9):
            return "равнобедренный", ""
        else:
            return "разносторонний", ""
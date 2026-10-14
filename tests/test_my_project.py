import unittest
from src.my_project import triangle


class TestTriangle(unittest.TestCase):

    def test_non_numeric_input_returns_error(self):
        t, coords = triangle("a", "b", "c")
        self.assertEqual(t, "")
        self.assertEqual(coords, [(-2, -2)] * 3)

    def test_partially_non_numeric_input_returns_error(self):
        t, _ = triangle("3", "x", "5")
        self.assertEqual(t, "")

    def test_zero_side_is_not_triangle(self):
        t, coords = triangle(0, 3, 4)
        self.assertEqual(t, "не треугольник")
        self.assertEqual(coords, [(-1, -1)] * 3)

    def test_negative_side_is_not_triangle(self):
        t, _ = triangle(-3, 4, 5)
        self.assertEqual(t, "не треугольник")

    def test_degenerate_triangle_is_not_triangle(self):
        t, _ = triangle(1, 2, 3)
        self.assertEqual(t, "не треугольник")

    def test_sum_less_than_third_side(self):
        t, _ = triangle(1, 1, 10)
        self.assertEqual(t, "не треугольник")

    def test_equilateral_triangle(self):
        t, _ = triangle(5, 5, 5)
        self.assertEqual(t, "равносторонний")

    def test_isosceles_triangle(self):
        t, _ = triangle(5, 5, 8)
        self.assertEqual(t, "равнобедренный")

    def test_isosceles_triangle_other_pair(self):
        t, _ = triangle(5, 8, 8)
        self.assertEqual(t, "равнобедренный")

    def test_scalene_triangle(self):
        t, _ = triangle(3, 4, 5)
        self.assertEqual(t, "разносторонний")

    def test_coordinates_for_equilateral(self):
        t, coords = triangle(10, 10, 10)
        self.assertEqual(t, "равносторонний")
        self.assertEqual(len(coords), 3)
        self.assertEqual(coords[0], (0, 0))
        self.assertEqual(coords[1][1], 0)  # вторая точка на оси X

    def test_coordinates_are_integers(self):
        _, coords = triangle(3, 4, 5)
        for x, y in coords:
            self.assertIsInstance(x, int)
            self.assertIsInstance(y, int)

    def test_third_point_has_positive_y(self):
        _, coords = triangle(3, 4, 5)
        self.assertGreater(coords[2][1], 0)

    def test_coordinates_fit_in_100_scale(self):
        _, coords = triangle(3, 4, 5)
        for x, y in coords:
            self.assertLessEqual(abs(x), 100)
            self.assertLessEqual(abs(y), 100)

    def test_float_strings_are_accepted(self):
        t, _ = triangle("3.0", "4.0", "5.0")
        self.assertEqual(t, "разносторонний")

    def test_almost_equal_sides_is_isosceles(self):
        t, _ = triangle(5, 5, 5.0000000001)
        self.assertIn(t, ["равносторонний", "равнобедренный"])
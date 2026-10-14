import unittest
import datetime
from src.delivery_service import calculate_delivery_cost


class TestDeliveryCost(unittest.TestCase):
    """Юнит-тесты для модуля расчета стоимости доставки."""

    def test_weight_below_minimum_returns_error(self):
        """Вес меньше 0.1 кг — ошибка."""
        self.assertEqual(
            calculate_delivery_cost(0.05, 100, "обычный"),
            (-1, "0000-00-00")
        )

    def test_weight_above_maximum_returns_error(self):
        """Вес больше 50 кг — ошибка."""
        self.assertEqual(
            calculate_delivery_cost(50.1, 100, "обычный"),
            (-1, "0000-00-00")
        )

    def test_weight_at_lower_boundary_is_accepted(self):
        """Вес ровно 0.1 кг — допустимо."""
        cost, _ = calculate_delivery_cost(0.1, 100, "обычный")
        self.assertGreater(cost, 0)

    def test_weight_at_upper_boundary_is_accepted(self):
        """Вес ровно 50 кг — допустимо."""
        cost, _ = calculate_delivery_cost(50.0, 100, "обычный")
        self.assertGreater(cost, 0)

    def test_distance_zero_returns_error(self):
        """Расстояние 0 км — ошибка."""
        self.assertEqual(
            calculate_delivery_cost(10, 0, "обычный"),
            (-1, "0000-00-00")
        )

    def test_distance_above_maximum_returns_error(self):
        """Расстояние больше 5000 км — ошибка."""
        self.assertEqual(
            calculate_delivery_cost(10, 5001, "обычный"),
            (-1, "0000-00-00")
        )

    def test_distance_at_boundaries_is_accepted(self):
        """Расстояние 1 км и 5000 км — допустимо."""
        self.assertGreater(calculate_delivery_cost(10, 1, "обычный")[0], 0)
        self.assertGreater(calculate_delivery_cost(10, 5000, "обычный")[0], 0)

    def test_invalid_package_type_returns_error(self):
        """Несуществующий тип посылки — ошибка."""
        self.assertEqual(
            calculate_delivery_cost(10, 100, "стеклянный"),
            (-1, "0000-00-00")
        )

    def test_all_valid_package_types_accepted(self):
        """Все три допустимых типа принимаются."""
        for t in ["обычный", "хрупкий", "опасный"]:
            cost, _ = calculate_delivery_cost(10, 100, t)
            self.assertGreater(cost, 0)

    def test_base_cost_for_light_regular_package(self):
        """Легкая обычная посылка: 200 + 100*5 = 700."""
        cost, _ = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_base_cost_for_minimum_distance(self):
        """Минимальное расстояние: 200 + 1*5 = 205."""
        cost, _ = calculate_delivery_cost(1.0, 1, "обычный")
        self.assertEqual(cost, 205)

    def test_weight_between_5_and_20_applies_1_2_coefficient(self):
        """Вес 10 кг: 700 * 1.2 = 840."""
        cost, _ = calculate_delivery_cost(10.0, 100, "обычный")
        self.assertEqual(cost, 840)

    def test_weight_over_20_applies_1_5_coefficient(self):
        """Вес 25 кг: 700 * 1.5 = 1050."""
        cost, _ = calculate_delivery_cost(25.0, 100, "обычный")
        self.assertEqual(cost, 1050)

    def test_weight_exactly_5_has_no_coefficient(self):
        """Вес ровно 5 кг — коэффициент не применяется: 700."""
        cost, _ = calculate_delivery_cost(5.0, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_weight_exactly_20_applies_1_5_coefficient(self):
        """Вес ровно 20 кг: 700 * 1.5 = 1050."""
        cost, _ = calculate_delivery_cost(20.0, 100, "обычный")
        self.assertEqual(cost, 1050)

    def test_fragile_package_adds_300(self):
        """Хрупкая: 700 + 300 = 1000."""
        cost, _ = calculate_delivery_cost(1.0, 100, "хрупкий")
        self.assertEqual(cost, 1000)

    def test_dangerous_package_adds_1000(self):
        """Опасная: 700 + 1000 = 1700."""
        cost, _ = calculate_delivery_cost(1.0, 100, "опасный")
        self.assertEqual(cost, 1700)

    def test_fragile_and_heavy_combined(self):
        """Хрупкая + вес 10 кг: 700 * 1.2 + 300 = 1140."""
        cost, _ = calculate_delivery_cost(10.0, 100, "хрупкий")
        self.assertEqual(cost, 1140)

    def test_express_should_be_more_expensive_than_regular(self):
        """ЭКСПРЕСС должен быть дороже обычной доставки."""
        regular, _ = calculate_delivery_cost(1.0, 100, "обычный", is_express=False)
        express, _ = calculate_delivery_cost(1.0, 100, "обычный", is_express=True)
        self.assertGreater(express, regular)

    def test_delivery_date_is_future(self):
        """Дата доставки позже даты отправки (2026-09-03)."""
        _, d = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertGreater(d, "2026-09-03")

    def test_express_delivery_is_not_zero_days(self):
        """Экспресс на короткое расстояние не должен давать 0 дней."""
        start = datetime.date(2026, 9, 3)
        _, d = calculate_delivery_cost(1.0, 100, "обычный", is_express=True)
        result = datetime.datetime.strptime(d, "%Y-%m-%d").date()
        self.assertGreaterEqual((result - start).days, 1)

    def test_long_distance_takes_more_days(self):
        """5000 км дольше, чем 500 км."""
        _, d1 = calculate_delivery_cost(1.0, 500, "обычный")
        _, d2 = calculate_delivery_cost(1.0, 5000, "обычный")
        self.assertGreater(d2, d1)

    def test_express_is_faster_than_regular(self):
        """Экспресс приходит раньше обычной доставки."""
        _, regular = calculate_delivery_cost(1.0, 5000, "обычный", is_express=False)
        _, express = calculate_delivery_cost(1.0, 5000, "обычный", is_express=True)
        self.assertLess(express, regular)


if __name__ == "__main__":
    unittest.main()
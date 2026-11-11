import unittest
from unittest.mock import Mock, patch

from src.calculator import TriangleCalculator
from src.database import TriangleDatabase
from src.controller import Controller
from src.user_interaction import UserInteraction, ConsoleUserInteraction
from src.external_service import ExternalService, EmailService


class TestCalculatorUnit(unittest.TestCase):

    def test_calculator_detects_equilateral(self):
        calc = TriangleCalculator()
        t, err = calc.compute(3, 3, 3)
        self.assertEqual(t, "равносторонний")
        self.assertEqual(err, "")

    def test_calculator_returns_error_message_for_invalid_data(self):
        calc = TriangleCalculator()
        t, err = calc.compute("a", "b", "c")
        self.assertEqual(t, "")
        self.assertIn("Нечисловые", err)


class TestDatabaseUnit(unittest.TestCase):
    """Юнит-тест БД: добавление, чтение, удаление."""

    def test_database_saves_and_reads_record(self):
        db = TriangleDatabase(":memory:")
        db.add(3, 4, 5, "разносторонний", "")
        self.assertEqual(db.get(3, 4, 5), ("разносторонний", ""))
        db.delete(3, 4, 5)
        self.assertIsNone(db.get(3, 4, 5))
        db.close()


class TestControllerIntegration(unittest.TestCase):

    def setUp(self):
        self.db = TriangleDatabase(":memory:")
        self.calc = TriangleCalculator()
        self.email = EmailService()

    def tearDown(self):
        self.db.close()


    def test_controller_computes_new_and_saves_to_db(self):
        user = Mock(spec=UserInteraction)
        user.get_input.return_value = ("3", "4", "5")

        controller = Controller(self.calc, self.db, user, self.email)
        result = controller.run()

        self.assertEqual(result["type"], "разносторонний")
        self.assertEqual(result["source"], "вычислено")
        # Запись реально попала в БД
        self.assertIsNotNone(self.db.get("3", "4", "5"))


    def test_controller_reads_from_db_on_second_call(self):
        user = Mock(spec=UserInteraction)
        user.get_input.return_value = ("3", "4", "5")

        controller = Controller(self.calc, self.db, user, self.email)
        controller.run()          # 1-й раз — вычисление
        second = controller.run() # 2-й раз — из БД

        self.assertEqual(second["source"], "из БД")
        self.assertEqual(second["type"], "разносторонний")


    def test_controller_sends_result_to_external_service(self):
        user = Mock(spec=UserInteraction)
        user.get_input.return_value = ("5", "5", "5")

        fake_email = Mock(spec=ExternalService)
        fake_email.send.return_value = True

        controller = Controller(self.calc, self.db, user, fake_email)
        controller.run()


        fake_email.send.assert_called_once()
        sent_message = fake_email.send.call_args[0][0]
        self.assertIn("равносторонний", sent_message)

    def test_controller_handles_invalid_input_and_saves_error(self):
        user = Mock(spec=UserInteraction)
        user.get_input.return_value = ("0", "3", "4")

        controller = Controller(self.calc, self.db, user, self.email)
        result = controller.run()

        self.assertEqual(result["type"], "не треугольник")
        self.assertIn("Ошибка", result["message"])


class TestUserInteractionIsolation(unittest.TestCase):

    def test_console_interaction_uses_input_calls(self):
        with patch("builtins.input", side_effect=["3", "4", "5"]):
            result = ConsoleUserInteraction().get_input()
        self.assertEqual(result, ("3", "4", "5"))

    def test_console_interaction_returns_three_values(self):
        with patch("builtins.input", return_value="1"):
            result = ConsoleUserInteraction().get_input()
        self.assertEqual(len(result), 3)
import logging
import math
import os
import sys
def configure_logging():
    os.makedirs("logs", exist_ok=True)

    log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("logs/file_txt.log", encoding="utf-8"),
        ],
    )
def triangle(s1, s2, s3):
    logging.info(f"Запрос: {s1}, {s2}, {s3}")


    try:
        a, b, c = float(s1), float(s2), float(s3)
    except ValueError:
        logging.error("Нечисловые данные")
        return "", [(-2, -2), (-2, -2), (-2, -2)]


    x, y, z = sorted([a, b, c])
    if a <= 0 or b <= 0 or c <= 0 or math.isclose(x + y, z, abs_tol=1e-9) or x + y < z:
        logging.info("Не треугольник")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]


    if math.isclose(a, b, abs_tol=1e-9) and math.isclose(b, c, abs_tol=1e-9):
        t = "равносторонний"
    elif math.isclose(a, b, abs_tol=1e-9) or math.isclose(b, c, abs_tol=1e-9) or math.isclose(a, c, abs_tol=1e-9):
        t = "равнобедренный"
    else:
        t = "разносторонний"


    cx = (a * a + c * c - b * b) / (2 * c)
    cy = math.sqrt(max(a * a - cx * cx, 0))


    scale = 100 / max(c, cy)

    coords = [
        (0, 0),
        (round(c * scale), 0),
        (round(cx * scale), round(cy * scale)),
    ]

    logging.info(f"Результат: {t}, координаты {coords}")
    return t, coords


def Main():
    logging.info("Приложение запущено")

    s1 = input("Сторона A: ")
    s2 = input("Сторона B: ")
    s3 = input("Сторона C: ")

    try:
        t, coords = triangle(s1, s2, s3)
        print(f"Тип: {t}")
        print(f"Координаты: {coords}")
    except Exception:
        logging.exception("Ошибка")

    logging.info("Приложение завершено")


if __name__ == "__main__":
    Main()


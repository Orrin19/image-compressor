"""Модуль прямоугольника"""


class Rectangle:
    """Прямоугольник, заданный координатами"""

    def __init__(self, bbox: tuple[int]) -> None:
        """Конструктор прямоугольника"""
        self.bbox = bbox
        self.xmin = bbox[0]
        self.xmax = bbox[0] + bbox[2]
        self.ymin = bbox[1]
        self.ymax = bbox[1] + bbox[3]

    def contains(self, x: int, y: int) -> bool: # pylint: disable=C0103
        """Проверка принадлежности точки прямоугольнику"""
        return self.xmin <= x <= self.xmax and self.ymin <= y <= self.ymax

    def intersects(self, other: 'Rectangle') -> bool:
        """Проверка пересечения прямоугольников"""
        return not (
            self.xmax < other.xmin or
            self.xmin > other.xmax or
            self.ymax < other.ymin or
            self.ymin > other.ymax
        )

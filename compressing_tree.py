"""Модуль сжимающего квадродерева"""


from threading import Thread
import numpy as np
from PIL import Image
from tree.quad_tree import QuadTree


class CompressingTree(QuadTree):
    """Класс сжимающего квадродерева"""

    RED_INTENSITY = 0.2989
    GREEN_INTENSITY = 0.5870
    BLUE_INTENSITY = 0.1140

    def __init__(
        self,
        image: Image.Image,
        bbox: tuple[int],
        depth: int = 0
    ) -> None:
        super().__init__(bbox, depth)
        self.leaf = False

        image = image.crop(bbox)
        hist = image.histogram()

        self.detail = self.get_detail_intensity(hist)
        self.color = self.get_average_color(image)

    def subdivide(self, image: Image.Image) -> None: # pylint: disable=W0221
        """Создание четырёх дочерних деревьев с использованием потоков"""
        left, top, width, height = self.boundary.bbox
        xcenter = left + (width - left) / 2
        ycenter = top + (height - top) / 2

        self.children = []
        threads = []

        for bbox in [
            (left, top, xcenter, ycenter),
            (xcenter, top, width, ycenter),
            (left, ycenter, xcenter, height),
            (xcenter, ycenter, width, height)
        ]:
            thread = Thread(
                target = self.add_child,
                args = (image, bbox, self.depth + 1)
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def add_child(
        self,
        image: Image.Image,
        bbox: tuple[int],
        depth: int = 0
    ) -> None:
        """Добавляет дочернее дерево"""
        child_tree = CompressingTree(image, bbox, depth)
        self.children.append(child_tree)

    @classmethod
    def get_average_color(cls, image: Image.Image) -> tuple[int]:
        """Возвращает средний цвет части изображения"""
        image_arr = np.asarray(image)
        avg_color = np.average(image_arr, axis=(0,1))
        return tuple(map(int, avg_color))

    @classmethod
    def get_deviation(cls, hist: list[int]) -> float:
        """Возвращает среднеквадратичное отклонение выборки"""
        total = sum(hist)
        deviation = value = 0

        if total > 0:
            value = sum(i * x for i, x in enumerate(hist)) / total
            deviation = \
                sum(x * (value - i) ** 2 for i, x in enumerate(hist)) / total
            deviation = deviation ** 0.5

        return deviation

    @classmethod
    def get_detail_intensity(cls, hist: list[int]) -> float:
        """Возвращает интенсивность детализации"""
        red_deviation = cls.get_deviation(hist[:256])
        green_deviation = cls.get_deviation(hist[256:512])
        blue_deviation = cls.get_deviation(hist[512:768])

        detail_intensity = \
            red_deviation * cls.RED_INTENSITY + \
            green_deviation * cls.GREEN_INTENSITY + \
            blue_deviation * cls.BLUE_INTENSITY

        return detail_intensity
    
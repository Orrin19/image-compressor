"""Модуль квадродерева"""


from tree.rectangle import Rectangle


class QuadTree:
    """Квадродерево"""

    QT_NODE_CAPACITY = 4

    def __init__(
        self,
        bbox: tuple[int],
        depth: int = 0
    ) -> None:
        """Конструктор квадродерева"""
        self.boundary = Rectangle(bbox)
        self.depth = depth
        self.points = []
        self.children = None

    def insert(self, x: int, y: int) -> bool: # pylint: disable=C0103
        """Вставка точки в дерево по заданным координатам"""
        if not self.boundary.contains(x, y):
            return False

        if (
            len(self.points) < self.QT_NODE_CAPACITY and
            self.children is None and
            (x, y) not in self.points
        ):
            self.points.append((x, y))
            return True

        if self.children is None:
            self.subdivide()

        for child in self.children:
            if child.insert(x, y):
                return True
        return False

    def remove(self, x: int, y: int) -> bool: # pylint: disable=C0103
        """Удаление точки из дерева по заданным координатам"""
        if not self.boundary.contains(x, y):
            return False

        if self.children is None:
            if (x, y) in self.points:
                self.points.remove((x, y))
                return True
            return False

        for child in self.children:
            if child.remove(x, y):
                return True
        return False

    def subdivide(self) -> None:
        """Создание четырёх дочерних деревьев"""
        left, top, width, height = self.boundary.bbox
        xcenter = left + width / 2
        ycenter = top + height / 2

        north_west = QuadTree(
            (left, top, width / 2, height / 2), self.depth + 1
        )
        north_east = QuadTree(
            (xcenter, top, width / 2, height / 2), self.depth + 1
        )
        south_west = QuadTree(
            (left, ycenter, width / 2, height / 2), self.depth + 1
        )
        south_east = QuadTree(
            (xcenter, ycenter, width / 2, height / 2), self.depth + 1
        )

        self.children = [north_west, north_east, south_west, south_east]

        for x, y in self.points: # pylint: disable=C0103
            for i, _ in enumerate(self.children):
                if self.children[i].insert(x, y):
                    break

        self.points = []

    def query_range(self, bbox: tuple[int]) -> list[tuple[int]]:
        """Поиск точек в заданном прямоугольнике"""
        query_range = Rectangle(bbox)
        points_in_range = []

        if not self.boundary.intersects(query_range):
            return points_in_range

        for x, y in self.points: # pylint: disable=C0103
            if query_range.contains(x, y):
                points_in_range.append((x, y))

        if self.children is None:
            return points_in_range

        for child in self.children:
            points_in_range.extend(
                child.query_range(bbox)
            )

        return points_in_range

"""Модуль для сжатия изображений с помощью квадродерева"""


from PIL import Image, ImageDraw
from compressing_tree import CompressingTree


class ImageCompressor():
    """Менеджер сжатия изображений с помощью квадродерева"""

    MAX_DEPTH = 8
    DETAIL_THRESHOLD = 15

    def __init__(
        self,
        image: Image.Image,
    ) -> None:
        self.width, self.height = image.size
        self.quadrants = []

        self.current_depth = 0
        self.root = CompressingTree(image, image.getbbox())

        self.build(self.root, image)

    def build(self, root: CompressingTree, image: Image.Image) -> None:
        """Создание сжимающего квадродерева до максимальной глубины"""
        if (
            root.depth >= self.MAX_DEPTH or
            root.detail <= self.DETAIL_THRESHOLD
        ):
            if root.depth > self.current_depth:
                self.current_depth = root.depth
            root.leaf = True
            return

        root.subdivide(image)

        for children in root.children:
            self.build(children, image)

    def create_image(
        self,
        custom_depth: int,
        show_lines: bool = False
    ) -> Image.Image:
        """Создание изображения, сжатого до указанной глубины"""
        image = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, self.width, self.height), (0, 0, 0))

        self.get_leaf_quadrants(custom_depth)

        for quadrant in self.quadrants:
            if show_lines:
                draw.rectangle(
                    quadrant.boundary.bbox,
                    quadrant.color,
                    outline = (0, 0, 0)
                )
            else:
                draw.rectangle(
                    quadrant.boundary.bbox,
                    quadrant.color
                )

        return image

    def get_leaf_quadrants(self, depth: int) -> list[CompressingTree]:
        """Получение списка квадрантов с указанной глубины"""
        if depth > self.current_depth:
            raise ValueError('A depth larger than the trees depth was given')

        self.recursive_search(self.root, depth)

    def recursive_search(
        self,
        quadrant: CompressingTree,
        max_depth: int
    ) -> None:
        """Рекурсивный поиск квадрантов с указанной глубины"""
        if quadrant.leaf or quadrant.depth == max_depth:
            self.quadrants.append(quadrant)
            return

        for child in quadrant.children:
            self.recursive_search(child, max_depth)

    def create_gif(
        self,
        file_name: str,
        duration: int = 1000,
        loop: int = 0,
        show_lines: bool = False
    ) -> None:
        """Создание gif-анимации сжатия изображения"""
        gif = []
        product_image = \
            self.create_image(self.current_depth, show_lines=show_lines)

        for i in range(self.current_depth, -1, -1):
            image = self.create_image(i, show_lines=show_lines)
            gif.append(image)

        gif.append(image)
        gif.insert(0, product_image)
        gif[0].save(
            file_name,
            save_all = True,
            append_images = gif[1:],
            duration = duration,
            loop = loop
        )

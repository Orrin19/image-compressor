"""Модуль консольного приложения"""


import argparse
from PIL import Image
from image_compressor import ImageCompressor


def configure_parser():
    """Создание и настройка объекта парсера"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i',
        '--image',
        type=str,
        dest='image',
        help='путь к файлу с изображением'
    )
    parser.add_argument(
        '-df',
        '--destination_file',
        type=str,
        dest='destination_file',
        help='путь к файлу назначения'
    )
    parser.add_argument(
        '-l',
        '--lines',
        type=bool,
        dest='lines',
        action=argparse.BooleanOptionalAction,
        help='флаг отрисовки линий квадрантов'
    )
    parser.add_argument(
        '-g',
        '--gif',
        type=bool,
        dest='gif',
        action=argparse.BooleanOptionalAction,
        help='флаг создания gif-анимации'
    )
    parser.add_argument(
        '-d',
        '--depth',
        type=int,
        dest='depth',
        help='глубина сжатия изображения (от 0 до 8)'
    )
    return parser


def create_gif(
    compressor: ImageCompressor,
    path: str = 'images/compressing.gif',
    show_lines: bool = False
) -> None:
    """Создание gif-анимации сжатия изображения"""
    compressor.create_gif(path, show_lines=show_lines)


def create_image(
    compressor: ImageCompressor,
    depth: int,
    path: str = 'images/compressed.jpg',
    show_lines: bool = False
) -> None:
    """Создание изображения, сжатого до указанной глубины"""
    img = compressor.create_image(depth, show_lines=show_lines)
    img.save(path)


def main():
    """Основная функция приложения"""
    parser = configure_parser()
    args = parser.parse_args()

    if not args.image:
        parser.print_help()
        return
    image_path = args.image

    destination_path = args.destination_file or \
        ('images/' + \
         image_path.split('/')[-1].split('.')[0] + \
         ('_compressing.gif' if args.gif else '_compressed.jpg'))

    lines = args.lines
    gif = args.gif

    depth = args.depth or 7
    if depth < 0 or depth > 8:
        print('Глубина сжатия должна быть в диапазоне от 0 до 8!')
        return

    try:
        img = Image.open(image_path)
        print('Ведётся сжатие изображения...')
        compressor = ImageCompressor(img)
    except FileNotFoundError:
        print('Файл не найден!')
        return

    if gif:
        create_gif(compressor, destination_path, lines)
        print('Анимация сжатия сохранена в ' + destination_path)
    else:
        create_image(compressor, depth, destination_path, lines)
        print('Сжатое изображение сохранено в ' + destination_path)


if __name__ == '__main__':
    main()

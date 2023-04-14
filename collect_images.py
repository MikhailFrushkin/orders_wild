import glob

from PIL import Image
from data.config import path

# Определяем размеры листа A4 в пикселях
A4_WIDTH = 2480
A4_HEIGHT = 3508

# Создаем пустой лист A4

# Определяем размеры изображений-значков и их количество
ICON_SIZE = int((37 / 25.4) * 420)
ICONS_PER_ROW = 4
ICONS_PER_COL = 5


def add_images(num):
    path_images = f'{path}/files/CHEBURASHKA-7NEW-4-37/Значки по отдельности/Уникальные значки/'
    files = glob.glob(path_images + '/*.png')
    print(files)
    print(f'Количество значков в папке: {len(files)}')
    print(f'Количество значков  в общем на {num} заказов: {len(files)*num}')
    all_images = len(files)*num
    num_page = len(files)*num // 20
    if len(files)*num % 20 > 0:
        num_page += 1
    print(f'Количество листов: {num_page}')
    for page in range(num_page):
        result_image = Image.new('RGB', (A4_WIDTH, A4_HEIGHT), (255, 255, 255))

        for i in range(0, ICONS_PER_ROW * ICONS_PER_COL, len(files)):

            if i > 20 or all_images == 0:
                break
            try:
                for file in files:
                    if all_images == 0:
                        break
                    icon_image = Image.open(file).convert('RGBA')
                    background = Image.new('RGBA', icon_image.size, (255, 255, 255, 255))
                    alpha_composite = Image.alpha_composite(background, icon_image)
                    icon_image = alpha_composite.crop(alpha_composite.getbbox())
                    icon_image = icon_image.resize((ICON_SIZE, ICON_SIZE))
                    # Вычисляем координаты для размещения изображения на листе A4
                    row = i // ICONS_PER_ROW
                    col = i % ICONS_PER_ROW
                    x = col * ICON_SIZE + (A4_WIDTH - ICON_SIZE * ICONS_PER_ROW) // 2
                    y = row * ICON_SIZE + (A4_HEIGHT - ICON_SIZE * ICONS_PER_COL) // 2

                    # Размещаем изображение на листе A4
                    result_image.paste(icon_image, (x, y))
                    i += 1
                    all_images -= 1
            except Exception as ex:
                print(ex)
        result_image.save(f'result{page}.png')



if __name__ == '__main__':
    add_images()

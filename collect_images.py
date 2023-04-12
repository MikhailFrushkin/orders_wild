from PIL import Image

# Определяем размеры листа A4 в пикселях
A4_WIDTH = 2480
A4_HEIGHT = 3508

# Создаем пустой лист A4
result_image = Image.new('RGB', (A4_WIDTH, A4_HEIGHT), (255, 255, 255))

# Определяем размеры изображений-значков и их количество
ICON_SIZE = int((37 / 25.4) * 360)
ICONS_PER_ROW = 4
ICONS_PER_COL = 5

# Загружаем изображения и обрезаем белый фон
for i in range(ICONS_PER_ROW * ICONS_PER_COL):
    icon_image = Image.open(
        f'/home/mikhail/PycharmProjects/generate_pdf/files/'
        f'IMPROVIZATSIYANABOR-10NEW-20-37/Значки по отдельности/Уникальные значки/{i + 1}.png').convert(
        'RGBA')
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

# Сохраняем результат
result_image.save('result.png')

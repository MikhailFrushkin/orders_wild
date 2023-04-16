import os

import cv2

from data.config import path


def split_image(filename, dirname, dict_orders):
    icon_dir = dirname
    image = cv2.imread(filename)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray_image, 240, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    scale_px_mm = 5  # 10 пикселей на 1 мм
    os.makedirs(icon_dir, exist_ok=True)
    count = 1
    size = None

    for i in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[i])

        diameter_px = max(w, h)
        diameter_mm = diameter_px / scale_px_mm
        if 150 > diameter_mm > 100:
            print(diameter_mm)
            size = 37
            icon = image[y:y + h, x:x + w]
            cv2.imwrite(f"{icon_dir}/Значки по отдельности/{count}.png", icon)
            count += 1
        elif 600 > diameter_mm > 200:
            size = 56
            print(f'большие значки {diameter_mm}')
            if w > h:  # vertical rectangle
                # split image into 3 equal parts vertically
                h1 = h // 3
                h2 = h1 * 2
                icon1 = image[y:y + h, x:x + w // 3]
                icon2 = image[y:y + h, x + w // 3:x + w // 3 * 2]
                icon3 = image[y:y + h, x + w // 3 * 2:x + w]
                cv2.imwrite(f"{icon_dir}/Значки по отдельности/{count}.png", icon1)
                count += 1
                cv2.imwrite(f"{icon_dir}/Значки по отдельности/{count}.png", icon2)
                count += 1
                cv2.imwrite(f"{icon_dir}/Значки по отдельности/{count}.png", icon3)
                count += 1
    try:
        name = os.path.splitext(os.path.basename(filename))[0]
        print(name)
        print(size)
        dict_orders[name]['size'] = size
    except Exception as ex:
        print(ex)
    print(dict_orders)


if __name__ == '__main__':
    dict_temp = {}
    split_image(f'{path}/files/KAPIBARANABOR-9NEW-6-56/KAPIBARANABOR-9NEW-6-56.jpg', 'Значки по отдельности', dict_temp)
    split_image(f'{path}/files/IMPROVIZATSIYANABOR-10NEW-20-37/IMPROVIZATSIYANABOR-10NEW-20-37.png',
                'Значки по отдельности', dict_temp)
    # split_image('IMPROVIZATSIYANABOR-10NEW-20-37.png')

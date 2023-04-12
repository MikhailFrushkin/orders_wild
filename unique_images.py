import hashlib
import os

import cv2
from PIL import Image
from skimage.metrics import structural_similarity as ssim


def unique_images_function(directory):
    hashes = {}
    unique_images = []
    # Задаем порог для SSIM
    ssim_threshold = 0.8

    # Проходимся по каждому изображению
    for i in range(1, len(os.listdir(directory)) + 1):
        # Открываем изображение и вычисляем его хеш
        with Image.open(f'icons/{i}.png') as img:
            hash = hashlib.md5(img.tobytes()).hexdigest()
            if hash in hashes:
                continue
            unique = True
            for j in range(1, i):
                img1 = cv2.imread(f'icons/{i}.png')
                img2 = cv2.imread(f'icons/{j}.png')

                gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
                gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

                h1, w1 = gray_img1.shape
                h2, w2 = gray_img2.shape

                # Если изображения имеют разные размеры, изменить размер одного или обоих изображений
                if h1 != h2 or w1 != w2:
                    # Найти наибольший размер
                    min_h, min_w = max(h1, h2), max(w1, w2)

                    gray_img1 = cv2.resize(gray_img1, (min_w, min_h))
                    gray_img2 = cv2.resize(gray_img2, (min_w, min_h))

                similarity_score = ssim(gray_img1, gray_img2)
                print(similarity_score)

                if similarity_score > ssim_threshold:
                    unique = False
                    break
            if unique:
                hashes[hash] = i
                unique_images.append(img)

    for img in unique_images:
        img.show()


if __name__ == '__main__':
    unique_images_function('/home/mikhail/PycharmProjects/generate_pdf/icons/')

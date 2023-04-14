import os

import pandas as pd

from data.config import path
from read_excel import read_excel_file
import glob

from split_image import split_image
from unique_images import unique_images_function


def search_folder(name):
    '''поиск папки по названию артикула'''
    for root, dirs, files in os.walk(path):
        if name in dirs:
            return os.path.join(root, name)
    return None


def df_to_dict():
    """Ищем папки по артикулам и добавляем их путь в словарь"""
    dict_orders = {}
    df_orders = pd.read_excel(f'{path}/Сгрупированный заказ.xlsx')
    df = df_orders.set_index('Артикул продавца')
    dict_from_df = df['Quantity'].to_dict()
    for key, value in dict_from_df.items():
        name_dir = search_folder(key)
        if name_dir:
            files = glob.glob(name_dir + '/*.png') + glob.glob(name_dir + '/*.jpg')
            if len(files) > 1:
                print('найшлось больше 1 файла со значками')
            name_image = files[0]
            dict_orders[key] = {'name_directory': name_dir, 'name_image': name_image, 'quantity': value, 'size': None}
        else:
            print(f'Не удалось найти папку для артикула: {key}')
    return dict_orders


def main():
    try:
        read_excel_file(f'{path}/Заказы.xlsx')
    except Exception as ex:
        print(f'ошибка чтения файла с заказами {ex}')
    dict_orders = df_to_dict()
    print(dict_orders)
    for key, value in dict_orders.items():
        directory = value['name_directory']  # указываем путь к директории
        name_image = value['name_image']
        folder_name = 'Значки по отдельности'  # указываем имя папки, которую нужно проверить/создать

        if not os.path.exists(os.path.join(directory, folder_name)):
            os.makedirs(os.path.join(directory, folder_name))
            print("Папка", folder_name, "была успешно создана в директории", directory)
            split_image(name_image, directory, dict_orders)
            unique_images_function(os.path.join(directory, folder_name))
        else:
            print("Папка", folder_name, "уже существует в директории", directory)


if __name__ == '__main__':
    main()
    # print(search_folder('BLACKPINK-5NEW-NABORxBLACK37'))

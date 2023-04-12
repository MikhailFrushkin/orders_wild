import os

import pandas as pd

from read_excel import read_excel_file


def search_folder(name):
    path = '/home/mikhail/PycharmProjects/generate_pdf/'
    '''поиск папки по названию артикула'''
    for root, dirs, files in os.walk(path):
        if name in dirs:
            return os.path.join(root, name)
    return None


def df_to_dict():
    """Ищем папки по артикулам и добавляем их путь в словарь"""
    dict_orders = {}
    df_orders = pd.read_excel('/home/mikhail/PycharmProjects/generate_pdf/Сгрупированный заказ.xlsx')
    df = df_orders.set_index('Артикул продавца')
    dict_from_df = df['Quantity'].to_dict()
    for key, value in dict_from_df.items():
        name_dir = search_folder(key)
        if name_dir:
            dict_orders[key] = (name_dir, value)
        else:
            print(f'Не удалось найти папку для артикула: {key}')
    return dict_orders


def main():
    read_excel_file('/home/mikhail/PycharmProjects/generate_pdf/Заказы.xlsx')

    dict_orders = df_to_dict()
    print(dict_orders)


if __name__ == '__main__':
    main()
    # print(search_folder('BLACKPINK-5NEW-NABORxBLACK37'))

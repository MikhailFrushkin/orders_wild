import pandas as pd


def read_excel_file(filename):
    list_columns = ['Название товара', 'Артикул Wildberries', 'Артикул продавца',
                    'Статус задания']
    df = pd.read_excel(filename, usecols=list_columns)

    df = df[df['Статус задания'] == 'Новое']

    grouped = df.groupby('Артикул продавца').agg(
        {'Артикул продавца': 'first', 'Артикул продавца': 'count'
         })
    grouped = grouped.rename(columns={'Артикул продавца': 'Quantity'})
    grouped_sorted = grouped.sort_values(by='Quantity', ascending=False)
    grouped_sorted.to_excel('Сгрупированный заказ.xlsx')


if __name__ == '__main__':
    read_excel_file('/home/mikhail/PycharmProjects/generate_pdf/Заказы.xlsx')

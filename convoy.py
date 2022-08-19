import pandas as pd
import csv
import re
import sqlite3 as sql


def file_name(_file: str) -> str:
    """
    Returns the filename without extension and CHECKED marker
    :param _file: Entered file name
    :return: File name
    """
    return _file.removesuffix('.csv').removesuffix('.xlsx').removesuffix('[CHECKED]')


file = input('Input file name\n')
# # file_name = ''
#
# if file.endswith('.xlsx'):
#     file_name = file.removesuffix('.xlsx')
#     my_df = pd.read_excel(f'{file}', sheet_name='Vehicles', dtype=str)
#     lines = my_df.shape[0]
#
#     my_df.to_csv(f'{file_name}.csv', index=None, header=True)
#
#     if lines == 1:
#         message = f'1 line was added to {file_name}.csv'
#     else:
#         message = f'{lines} lines were added to {file_name}.csv'
#
#     print(message)
# else:
#     file_name = file.removesuffix('.csv')
#
# _cell = 0
# with open(f'{file_name}.csv', newline='') as f:
#     f_reader = csv.reader(f, delimiter=',')
#     f_checked = []
#     index = 0
#     for line in f_reader:
#         if index == 0:
#             f_checked.append(line)
#             index += 1
#         else:
#             new_line = []
#             for el in line:
#                 new_el = re.findall(r'\d+', el)[0]
#                 new_line.append(int(new_el))
#
#                 if len(el) != len(new_el):
#                     _cell += 1
#
#             f_checked.append(new_line)
#
# with open(f'{file_name}[CHECKED].csv', 'w', encoding='utf-8') as f:
#     f_writer = csv.writer(f, delimiter=',', lineterminator='\n')
#     for line in f_checked:
#         f_writer.writerow(line)
#
# if _cell == 1:
#     message = f'1 cell was corrected in {file_name}[CHECKED].csv'
# else:
#     message = f'{_cell} cells were corrected in {file_name}[CHECKED].csv'
#
# print(message)
#
# conn = sql.connect(f'{file_name}.s3db')
# cursor_name = conn.cursor()

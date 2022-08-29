import pandas as pd
import csv
import re


def file_name(_file: str) -> str:
    """
    Returns the filename without extension and CHECKED marker
    :param _file: Entered file name
    :return: File name
    """
    return _file.removesuffix('.csv').removesuffix('.xlsx').removesuffix('[CHECKED]')


def xlsx_to_csv(_file: str, _file_name: str) -> int:
    """
    Will convert .xlsx to .csv file and return the number of lines added
    :param _file: Entered file name
    :param _file_name: The filename without extension and CHECKED marker
    :return: The number of lines added
    """
    my_df = pd.read_excel(f'{_file}', sheet_name='Vehicles', dtype=str)
    my_df.to_csv(f'{_file_name}.csv', index=None, header=True)
    return my_df.shape[0]


def corrected_data(_file_name: str) -> (list, int):
    """
    Corrects the table data and saves it to a list, counts the number of changed cells and returns these entities
    :param _file_name: The filename without extension and CHECKED marker
    :return _data_list: The clean data in list format
    :return _cells: The number of changed cells
    """
    _cells = 0
    _data_list = []

    with open(f'{_file_name}.csv', newline='') as f:
        f_reader = csv.reader(f, delimiter=',')
        index = 0
        for line in f_reader:
            if index == 0:
                _data_list.append(line)
                index += 1
            else:
                new_line = []
                for el in line:
                    new_el = re.findall(r'\d+', el)[0]
                    new_line.append(int(new_el))

                    if len(el) != len(new_el):
                        _cells += 1

                _data_list.append(new_line)

    return _data_list, _cells


def writer_csv(_data_list: list, _file_name: str):
    """
    Writes empty data to csv file
    :param _file_name: The filename without extension and CHECKED marker
    :param _data_list: The clean data in list format
    :return:
    """
    with open(f'{_file_name}[CHECKED].csv', 'w', encoding='utf-8') as f:
        f_writer = csv.writer(f, delimiter=',', lineterminator='\n')
        for line in _data_list:
            f_writer.writerow(line)

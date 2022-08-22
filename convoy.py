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


def lines_message(_lines: int, _file_name: str):
    """
    Message about the number of added lines
    :param _lines: The number of lines added
    :param _file_name: The filename without extension and CHECKED marker
    :return: Message about the number of added lines
    """
    message = f'{_lines} lines were added to {_file_name}.csv'
    if _lines == 1:
        message = f'1 line was added to {_file_name}.csv'
    print(message)


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


def cells_message(_cells: int, _file_name: str):
    """
    Message about the number of corrected cells
    :param _cells: The number of changed cells
    :param _file_name: The filename without extension and CHECKED marker
    :return: Message about the number of corrected cells
    """
    if _cells == 1:
        message = f'1 cell was corrected in {_file_name}[CHECKED].csv'
    else:
        message = f'{_cells} cells were corrected in {_file_name}[CHECKED].csv'
    print(message)


def for_database(_file_name: str) -> (list, int):
    """
    Creates a list of tuples to add to the database and returns the number of rows of data
    :param _file_name: The filename without extension and CHECKED marker
    :return: List of tuples to add to the database, number of data rows
    """
    with open(f'{_file_name}[CHECKED].csv', newline='') as f:
        f_reader = csv.reader(f, delimiter=',')
        index = 0
        data_list = []
        for line in f_reader:
            if index == 0:
                index += 1
            else:
                data_list.append(tuple(line))

    return data_list, len(data_list)


def db_message(_rows: int, _file_name: str):
    """
    Reports the number of rows inserted
    :param _rows: The number of data rows
    :param _file_name: The filename without extension and CHECKED marker
    :return: Message about the number of rows inserted
    """
    if _rows == 1:
        message = f'1 record was inserted into {_file_name}.s3db'
    else:
        message = f'{_rows} records were inserted into {_file_name}.s3db'
    print(message)


file = input('Input file name\n')
f_name = file_name(file)

if file.count('[CHECKED]') == 0:
    if file.endswith('.xlsx'):
        lines = xlsx_to_csv(file, f_name)
        lines_message(lines, f_name)

    data, cells = corrected_data(f_name)
    writer_csv(data, f_name)
    cells_message(cells, f_name)

try:
    conn = sql.connect(f'{f_name}.s3db')
    cur = conn.cursor()

    create_table_query = '''
    CREATE TABLE convoy(
    'vehicle_id' INTEGER PRIMARY KEY,
    'engine_capacity' INTEGER NOT NULL,
    'fuel_consumption' INTEGER NOT NULL,
    'maximum_load' INTEGER NOT NULL
    );
    '''

    cur.execute(create_table_query)

    data, number_rows = for_database(f_name)
    cur.executemany('INSERT INTO convoy VALUES(?, ?, ?, ?)', data)
    conn.commit()
    db_message(number_rows, f_name)

    cur.close()

except sql.Error as error:
    print("DB ERROR!!!", error)
finally:
    if conn:
        conn.close()

import csv


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

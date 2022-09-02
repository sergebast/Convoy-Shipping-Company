import csv
from math import floor


def for_database(_file_name: str) -> (list, int):
    """
    Creates a list of tuples to add to the database
    :param _file_name: The filename without extension and CHECKED marker
    :return: List of tuples to add to the database
    """
    with open(f'{_file_name}[CHECKED].csv', newline='') as f:
        f_reader = csv.reader(f, delimiter=',')
        index = 0
        data_list = []
        for line in f_reader:
            if index == 0:
                index += 1
            else:
                data_list.append(score(line))

    return data_list


def m_load(_maximum_load):
    if _maximum_load >= 20:
        return 2
    return 0


def fuel(_fuel_consumption):
    total = _fuel_consumption * 4.5
    if total <= 230:
        return 2
    return 1


def pitstops(_fuel_consumption, _engine_capacity):
    total = floor(_fuel_consumption * 4.5 / _engine_capacity)
    if total >= 2:
        return 0
    elif total == 1:
        return 1
    return 2


def score(_line: str) -> tuple:
    vehicle_id, engine_capacity, fuel_consumption, maximum_load = _line
    scr = pitstops(int(fuel_consumption), int(engine_capacity)) + fuel(int(fuel_consumption)) + m_load(int(maximum_load))

    return int(vehicle_id), int(engine_capacity), int(fuel_consumption), int(maximum_load), scr


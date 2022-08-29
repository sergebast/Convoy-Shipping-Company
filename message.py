mess = {
    "lines": [
        '1 line was added to {}.csv',
        '{} lines were added to {}.csv'
    ],
    "cells": [
        '1 cell was corrected in {}[CHECKED].csv',
        '{} cells were corrected in {}[CHECKED].csv'
    ],
    "db": [
        '1 record was inserted into {}.s3db',
        '{} records were inserted into {}.s3db'
    ],
    "json": [
        '1 vehicle was saved into {}.json',
        '{} vehicles were saved into {}.json'
    ]
}


def message_string(_type: str, _number: int, _file_name='test_file') -> str:
    """
    Returns a message about the number of items added/changed
    :param _type: Entity type being processed
    :param _number: The number of added/changed elements
    :param _file_name: The filename without extension and CHECKED marker
    :return: The message about the number of items added/changed
    """
    if _number == 1:
        return mess[_type][0].format(_file_name)
    return mess[_type][1].format(_number, _file_name)


def pm(_type: str, _number: int, _file_name='test_file'):
    """
    Print message
    :param _type: Entity type being processed
    :param _number: The number of added/changed elements
    :param _file_name: The filename without extension and CHECKED marker
    :return:
    """
    print(message_string(_type, _number, _file_name))

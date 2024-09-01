import json
import os
from enum import Enum


class Themes(Enum):
    dark = 0
    light = 1


def str_to_int(string):
    if string == '' or string == '0':
        return 0
    elif string[0] == '-':
        return 0 - int(string[1:])
    else:
        return int(string[1:])


def input_settings():
    try:
        with open(os.getcwd() + '\\_internal\\settings.json', 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        try:
            with open('newfile.txt', 'w') as file:
                data = {
                    'theme': 0,
                    'window_size': [882, 982],
                    'window_position': [0, 0]
                }
                json.dump(data, file)
                return data
        except FileNotFoundError:
            data = {
                'theme': 0,
                'window_size': [882, 982],
                'window_position': [0, 0]
            }
            return data


def export_settings(theme, position, size):
    try:
        with open(os.getcwd() + '\\_internal\\settings.json', 'w') as file:
            data = {
                'theme': theme,
                'window_size': size,
                'window_position': position
            }
            json.dump(data, file)
    except FileNotFoundError:
        print('File not found')

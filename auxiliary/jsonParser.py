import json
from auxiliary import data_frame as df


def json_to_character_sheet(path):
    try:
        with (open(path, 'r', encoding='utf-8') as input_file):
            data = json.load(input_file)
            data_frame = df.CharacterSheetData()
            data_frame.create_from_json(data)
            return data_frame
    except Exception as inst:
        print(type(inst))
        print(inst.args)
        print(inst)


def json_from_db_to_character_sheet(data):
    data_frame = df.CharacterSheetData()
    data = json.loads(data)
    data_frame.create_from_json(data)
    return data_frame


def character_sheet_to_json(path, data_frame):
    try:
        with open(path, 'w') as output_file:
            json.dump(data_frame, output_file)
    except Exception as inst:
        print(type(inst))
        print(inst.args)
        print(inst)

import json
import dataFrame


def xml_to_character_sheet(path):
    try:
        with (open(path, 'r', encoding='utf-8') as input_file):
            data = json.load(input_file)
            data_frame = dataFrame.CharacterSheetData()
            data_frame.create_from_json(data)
            # print(data_frame)

            print(json.dumps(data, indent=4))

            return data_frame
    except Exception as inst:
        print(type(inst))
        print(inst.args)
        print(inst)

def character_sheet_to_xml(path, data_frame):
    try:
        with open(path, 'w') as output_file:
            json.dump(data_frame, output_file)
    except Exception as inst:
        print(type(inst))
        print(inst.args)
        print(inst)
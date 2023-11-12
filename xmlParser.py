import json
import dataFrame


def xml_parser(path):
    try:
        with (open(path, 'r', encoding='utf-8') as input_file):
            data = json.load(input_file)
            data_frame = dataFrame.CharacterSheetData()
            data_frame.create_from_json(data)
            # print(data_frame)

            print(json.dumps(data, indent=4))

            return data_frame



            # test = dataFrame.Skills()
            # test.create_from_json(data)
            # print(test)
            #
            # test = dataFrame.Abilities()
            # test.create_from_json(data)
            # print(test)
            #
            # test = dataFrame.General()
            # test.create_from_json(data)
            # print(test)



    except Exception as inst:
        print(type(inst))
        print(inst.args)
        print(inst)

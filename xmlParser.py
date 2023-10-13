import json

import dataFrame


def xml_parser(path):
    try:
        with (open(path, 'r') as input_file):
            data = json.load(input_file)
            # print(json.dumps(data, indent=4))

            test = dataFrame.Skills()
            test.create_from_json(data)
            print(test)

            test = dataFrame.Abilities()
            test.create_from_json(data)
            print(test)

    except Exception as inst:
        print(type(inst))
        print(inst.args)
        print(inst)

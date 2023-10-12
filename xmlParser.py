import json


def xml_parser(path):
    try:
        with open(path, 'r') as input_file:
            data = json.load(input_file)
            print(json.dumps(data, indent=4))

    except Exception as inst:
        print(type(inst))
        print(inst.args)
        print(inst)


from parsed import Parsed


def ini_parse(file_content):
    # read file lines
    file_lines = file_content.readlines()

    # parsed dict
    parsed = Parsed()

    # for parents
    new_parent = False

    for line in file_lines:
        if line[0] == "[" and line[len(line) - 2] == "]":
            parent = line[1: len(line) - 2]
            parsed.add_parent(parent)
            #parsed[parent] = {}
            new_parent = True
        
        elif new_parent and line.count("=") == 1:
            if " = " in line:
                key, val = line.split(" = ")
            elif "=" in line:
                key, val = line.split("=")

            val = val.replace("\n", "").replace("\r", "")

            # check if digit
            if val.isdigit():
                val = int(val) 

            parsed.add(parent, key, val)
            #parsed[parent][key] = val

        elif line[0] == ";" or line.strip() == '':
            pass

        else:
            raise Exception("Not a valid ini file")

    return parsed.parsed_dict

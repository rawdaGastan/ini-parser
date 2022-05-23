
def ini_parse(file):
    # read file lines
    file_lines = file.readlines()

    # parsed dict
    parsed = {}

    # for parents
    new_parent = False

    for line in file_lines:
        if line[0] == "[":
            parent = line[1: len(line) - 2]
            parsed[parent] = {}
            new_parent = True
        
        elif new_parent and "=" in line:
            key, val = line.split(" = ")
            val = val.replace("\n", "").replace("\r", "")

            # check if digit
            if val.isdigit():
                val = int(val) 

            parsed[parent][key] = val

        elif line == "\n":
            pass

        else:
            raise Exception("Not a valid ini file")

    return parsed
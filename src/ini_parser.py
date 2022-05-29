
class Parser:

  def __init__(self):
    self.parsed_dict = {}

  def __add_parent(self, parent):
    # check if we have a parent
    if parent == None:
      raise Exception("KeyError: None")

    # check if the parent does not exist in the parsed dict
    if parent not in self.parsed_dict.keys():
      self.parsed_dict[parent] = {}

  def __add(self, parent, key, value):
    # add the parent first
    self.__add_parent(parent)

    # check if we have a key
    if key == None:
      raise Exception("KeyError: None")

    self.parsed_dict[parent][key] = value
  

  def to_string(self):
    #clean str
    parsed_str = ""

    # parse to str
    for parent, dict in self.parsed_dict.items():
      parsed_str += "[" + str(parent) + "]\n"
      for key, val in dict.items():
        parsed_str += str(key) + " = " + str(val) + "\n"

    return parsed_str


  def from_string(self, content):
    self.parsed_dict = {}

    # read file lines
    if(type(content) == str):
      file_lines = content.splitlines()
    else:
      file_lines = content.readlines()

    # for parents
    new_parent = False

    for line in file_lines:
        line = line.replace("\n", "").replace("\r", "")

        if len(line) > 0 and line[0] == "[" and line[len(line) - 1] == "]":
            parent = line[1: len(line) - 1]
            self.__add_parent(parent)
            new_parent = True
        
        elif len(line) > 0 and new_parent and line.count("=") == 1 and line[0] not in ["", "="] and line[len(line)-1] != "=":
            if " = " in line:
                key, val = line.split(" = ")
            elif "=" in line:
                key, val = line.split("=")

            # check if digit
            if val.isdigit():
                val = int(val) 

            self.__add(parent, key, val)

        elif len(line) > 0 and line[0] == ";" or line.strip() == '':
            continue

        else:
            raise Exception("Not a valid ini content")

    return self.parsed_dict


  def get_sections(self):
    self.sections = self.parsed_dict.keys()

    if len(list(self.sections)) == 0:
      raise Exception("There is no parsed data")

    return list(self.sections)


file_content = """
[owner]
name=John
organization = threefold

[database]
server = 192.0.2.62
port = 143
password = 123456
"""
parser = Parser()
dict = parser.from_string(file_content)
print(dict)
print(parser.to_string())

class Parser:

  def __init__(self):
    self.parsed_dict = {}
    self.parsed_str = ""

  def set_parsed_dict(self, parsed_dict):
    self.parsed_dict = parsed_dict
    self.get_sections()


  def add_parent(self, parent):
    # check if the parent does not exist in the parsed dict
    if parent not in self.parsed_dict.keys():
      self.parsed_dict[parent] = {}

  def add(self, parent, key, value):
    self.parsed_dict[parent][key] = value
  

  def to_string(self):
    #clean str
    self.parsed_str = ""

    # parse to str
    for parent, dict in self.parsed_dict.items():
      self.parsed_str += "[" + str(parent) + "]\n"
      for key, val in dict.items():
        self.parsed_str += str(key) + " = " + str(val) + "\n"

    return self.parsed_str


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
            self.add_parent(parent)
            new_parent = True
        
        elif len(line) > 0 and new_parent and line.count("=") == 1 and line[0] not in ["", "="] and line[len(line)-1] != "=":
            if " = " in line:
                key, val = line.split(" = ")
            elif "=" in line:
                key, val = line.split("=")

            # check if digit
            if val.isdigit():
                val = int(val) 

            self.add(parent, key, val)

        elif len(line) > 0 and line[0] == ";" or line.strip() == '':
            pass

        else:
            raise Exception("Not a valid ini file")

    self.get_sections()
    return self.parsed_dict


  def get_sections(self):
    self.sections = self.parsed_dict.keys()
    return list(self.sections)
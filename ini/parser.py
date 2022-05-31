
class Parser:

  def __init__(self):
    self.__parsed_dict = {}

  @property
  def parsed_dict(self):
      return self.__parsed_dict

  ###################
  # inner functions #
  ###################

  def __add_parent(self, parent):
    # check if we have a parent
    if not parent:
      raise Exception("KeyError: None")

    # check if the parent does not exist in the parsed dict
    if parent not in self.__parsed_dict.keys():
      self.__parsed_dict[parent] = {}

  def __add(self, parent, key, value):
    # add the parent first
    self.__add_parent(parent)

    # check if we have a key
    if not key:
      raise Exception("KeyError: None")

    self.__parsed_dict[parent][key] = value
  
  ###################
  #  user functions #
  ###################

  def __str__(self):
    #clean str
    parsed_str = ""

    # parse to str
    for parent, dict in self.__parsed_dict.items():
      parsed_str += "[" + str(parent) + "]\n"
      for key, val in dict.items():
        parsed_str += str(key) + " = " + str(val) + "\n"

    return parsed_str

  def save_to_file(self, path):
    """
    saves the parsed dict as ini file in the specified path after converting to string
    """
    with open(path, "a") as f:
      f.write(str(self))


  def from_string(self, content):
    self.__parsed_dict = {}

    # read content lines
    if(type(content) == str):
      file_lines = content.splitlines()
    else:
      file_lines = content.readlines()

    # for parents
    new_parent = False

    for line in file_lines:
        line = line.replace("\n", "").replace("\r", "")

        if len(line) > 0:
            #parse sections
            if line[0] == "[" and line[len(line) - 1] == "]":
                #check opened and closed section []
                if line.count('[') == 1 and line.count(']') == 1:
                    parent = line[1: len(line) - 1]
                    self.__add_parent(parent)
                    new_parent = True

                else:
                    raise Exception("Invalid section! Please make sure that you have one '[' and one ']'")

            #parse sections values
            elif new_parent and line.count("=") == 1 and (line[0] and line[len(line)-1] not in ["", "=", " "]):
                if " = " in line:
                    key, val = line.split(" = ")
                elif "=" in line:
                    key, val = line.split("=")

                # check if digit
                if val.isdigit():
                    val = int(val) 

                self.__add(parent, key, val)

            # parse comment lines
            elif line[0] == ";":
                continue

            # invlid content
            else:
                raise Exception("Not a valid ini content")
        
        # parse empty
        elif line.strip() == '':
            continue
        
        # invlid content
        else:
            raise Exception("Not a valid ini content")

  def to_dict(self):
    return self.__parsed_dict


  def get_sections(self):
    """
    returns a list of all sections --> [section1, section2, ...]
    """
    sections = self.__parsed_dict.keys()

    # if no data in the parsed dict
    if len(list(sections)) == 0:
      raise Exception("There is no parsed data")

    return list(sections)

  def get_section(self, section_key):
    """
    returns a dictionary for the section given --> {key1: val1, key2: val2, ....}
    """
    sections = self.get_sections()

    # if no data in the parsed dict
    if section_key not in sections:
      raise Exception("This section does not exist")

    else:
      section = self.__parsed_dict[section_key]

    return section

  def get_options(self, section_key):
    """
    returns all options of the given section
    """
    section = self.get_section(section_key)
    options = list(section.keys())

    # if no data in the parsed dict
    if len(options) == 0:
      raise Exception("This section does not have any options")

    return options

  def get_option(self, section_key, option_key):
    """
    returns the value of the option key which belongs to the section key given
    """
    section = self.get_options(section_key)

    # if no data in the parsed dict
    if option_key not in section:
      raise Exception("This option does not exist in the given section")

    else:
      option = self.__parsed_dict[section_key][option_key]

    return option

  def set_option(self, section_key, option_key, option_value):
    """
    update the option in the given section
    """
    section = self.get_options(section_key)

    # if no data in the parsed dict
    if option_key not in section:
      raise Exception("This option does not exist in the given section")

    else:
      self.__parsed_dict[section_key][option_key] = option_value


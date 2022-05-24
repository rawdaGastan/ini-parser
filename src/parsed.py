import json

class Parsed:

  def __init__(self):
    self.parsed_dict = {}

  def set_parsed_dict(self, parsed_dict):
    self.parsed_dict = parsed_dict


  def add_parent(self, parent):
    # check if the parent does not exist in the parsed dict
    if parent not in self.parsed_dict.keys():
      self.parsed_dict[parent] = {}

  def add(self, parent, key, value):
    self.parsed_dict[parent][key] = value
  

  def to_string(self):
    self.parsed_str = json.dumps(self.parsed_dict)


  def from_string(self, parsed_str):
    self.parsed_dict = json.loads(parsed_str)


  def get_sections(self):
    self.sections = self.parsed_dict.keys()

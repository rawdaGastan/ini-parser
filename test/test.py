import pytest
import os

#append src folder
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

from parse import ini_parse

# get the file location and name
file_name = "sample.ini"
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
file = open(os.path.join(__location__, file_name))

parsed = ini_parse(file)

# test functions
def test_value():
    assert parsed["owner"]["name"] == "John", "Should be John"
    assert parsed["owner"]["organization"] == "threefold", "Should be threefold"
    assert parsed["database"]["server"] == "192.0.2.62", "Should be 192.0.2.62"
    assert parsed["database"]["port"] == 143, "Should be 143"
    assert parsed["database"]["password"] == 123456, "Should be 123456"



import pytest
import os

#append src folder
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

from parse import ini_parse
from parsed import Parsed

# get the file location and name
file_name = "sample.ini"
wrong_file_name = "sample wrong.ini"

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def test_valid():
    file_content = open(os.path.join(__location__, file_name))
    try:
        ini_parse(file_content)
        assert True
    except Exception as exc:
        assert False

def test_in_valid():
    file_content = open(os.path.join(__location__, wrong_file_name))
    try:
        ini_parse(file_content)
        assert False
    except Exception as exc:
        assert True

def test_value():
    file_content = open(os.path.join(__location__, file_name))
    parsed = ini_parse(file_content)
    assert parsed["owner"]["name"] == "John", "Should be John"
    assert parsed["owner"]["organization"] == "threefold", "Should be threefold"
    assert parsed["database"]["server"] == "192.0.2.62", "Should be 192.0.2.62"
    assert parsed["database"]["port"] == 143, "Should be 143"
    assert parsed["database"]["password"] == 123456, "Should be 123456"

def test_parsed_sections():
    file_content = open(os.path.join(__location__, file_name))
    parsed = ini_parse(file_content)

    test_parsed = Parsed()
    test_parsed.set_parsed_dict(parsed)

    # get sections
    test_parsed.get_sections()
    test_parsed_sections = test_parsed.sections

    assert test_parsed_sections == ['owner', 'database']

def test_parsed_functions():
    file_content = open(os.path.join(__location__, file_name))
    parsed = ini_parse(file_content)

    test_parsed = Parsed()
    test_parsed.set_parsed_dict(parsed)
    #parsed str
    test_parsed.to_string()
    test_parsed_str = test_parsed.parsed_str
    
    # parsed dict
    test_parsed.from_string(test_parsed_str)
    test_parsed_dict = test_parsed.parsed_dict

    assert test_parsed_dict == parsed

    


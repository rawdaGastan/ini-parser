#####################
# append src folder #
#####################

import sys
import os

from pyparsing import unicodeString
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

from ini_parser import Parser

# get the file location and name
file_name = "sample.ini"

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


##################
# test functions #
################## 

def test_valid():
    file_content = open(os.path.join(__location__, file_name))
    parser = Parser()
    try:
        parser.from_string(file_content)
        assert True
    except Exception as exc:
        assert False


def test_value():
    file_content = open(os.path.join(__location__, file_name))
    parser = Parser()
    parsed = parser.from_string(file_content)
    assert parsed["owner"]["name"] == "John", "Should be John"
    assert parsed["owner"]["organization"] == "threefold", "Should be threefold"
    assert parsed["database"]["server"] == "192.0.2.62", "Should be 192.0.2.62"
    assert parsed["database"]["port"] == 143, "Should be 143"
    assert parsed["database"]["password"] == 123456, "Should be 123456"

def test_parsed_sections():
    file_content = open(os.path.join(__location__, file_name))
    parser = Parser()
    parsed = parser.from_string(file_content)

    test_parser = Parser()
    test_parser.set_parsed_dict(parsed)

    # get sections
    assert list(test_parser.sections) == list(parser.sections)


def test_parsed_functions():
    file_content = open(os.path.join(__location__, file_name))
    parser = Parser()
    parsed = parser.from_string(file_content)

    test_parsed = Parser()
    test_parsed.set_parsed_dict(parsed)

    #parsed str
    test_parsed_str = test_parsed.to_string()
    
    # parsed dict
    test_parsed_dict = test_parsed.from_string(test_parsed_str)

    assert test_parsed_dict == parsed

##################
# test invalid   #
################## 

def test_in_valid():
    parser = Parser()
    try:
        parser.from_string("[owner]\n--")
        assert False
    except Exception as exc:
        assert True

def test_unclosed_section():
    parser = Parser()
    try:
        parser.from_string("[owner\nkey=val\n")
        assert False
    except Exception as exc:
        assert True

def test_no_equal():
    parser = Parser()
    try:
        parser.from_string("[owner]\nkeyval\n")
        assert False
    except Exception as exc:
        assert True

def test_no_value():
    parser = Parser()
    try:
        parser.from_string("[owner]\nkeyval=\n")
        assert False
    except Exception as exc:
        assert True

def test_no_key():
    parser = Parser()
    try:
        parser.from_string("[owner]\n=keyval\n")
        assert False
    except Exception as exc:
        assert True

def test_more_then_one_equal():
    parser = Parser()
    try:
        parser.from_string("[owner]\nkey==val\n")
        assert False
    except Exception as exc:
        assert True


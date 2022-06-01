from ini.parser import Parser
import pytest

##################
# sample_content #
################## 

sample_content = {
#valid options
"valid": 
"""
[owner]
name=John
organization = threefold

[database]
server = 192.0.2.62
port = 143
password = 123456
protected = true
version = 12.6
""",

"valid_comment": ";comment",
"valid_empty": "",

#invalid options
"invalid": "[owner]\n--",
"invalid_section": "[[owner]", 
"invalid_unclosed_section": "[owner\nkey=val\n",
"invalid_unopened_section": "owner]\nkey=val\n",
"invalid_no_equal": "[owner]\nkeyval",
"invalid_no_value": "[owner]\nkeyval=",
"invalid_no_key": "[owner]\n=keyval",
"invalid_more_then_one_equal": "[owner]\nkey==val",

"invalid_no_sections": "",
"invalid_no_options": "[owner]",
}

##################
# test functions #
################## 
def test_valid():
    try:
        parser = Parser()
        parser.from_string(sample_content["valid"])
        assert True
    except Exception as exc:
        assert False

def test_valid_comment():
    try:
        parser = Parser()
        parser.from_string(sample_content["valid_comment"])
        assert True
    except Exception as exc:
        assert False

def test_valid_empty():
    try:
        parser = Parser()
        parser.from_string(sample_content["valid_empty"])
        assert True
    except Exception as exc:
        assert False

def test_value():
    parser = Parser()
    parser.from_string(sample_content["valid"])

    assert parser.get_option("owner", "name") == "John"
    assert parser.get_option("owner", "organization") == "threefold"
    assert parser.get_option("database", "server") == "192.0.2.62"
    assert parser.get_option("database", "port") == "143"
    assert parser.get_option("database", "password") == "123456"
    assert parser.get_option("database", "protected") == "true"
    assert parser.get_option("database", "version") == "12.6"

    assert parser.get_bool("database", "protected") == True
    assert parser.get_int("database", "port") == 143
    assert parser.get_float("database", "port") == 143
    assert parser.get_int("database", "password") == 123456
    assert parser.get_float("database", "version") == 12.6

def test_parsed_sections():
    parser = Parser()
    parser.from_string(sample_content["valid"])

    assert ["owner", "database"] == parser.get_sections()

def test_parsed_section():
    parser = Parser()
    parser.from_string(sample_content["valid"])

    assert parser.to_dict()["owner"] == parser.get_section("owner")

def test_parsed_options():
    parser = Parser()
    parser.from_string(sample_content["valid"])

    assert ["name", "organization"] == parser.get_options("owner")

def test_parsed_option():
    parser = Parser()
    parser.from_string(sample_content["valid"])

    assert parser.to_dict()["owner"]["name"] == parser.get_option("owner", "name")

def test_set_option():
    parser = Parser()
    parser.from_string(sample_content["valid"])
    parser.set_option("owner", "name", "Ali")

    assert "Ali" == parser.get_option("owner", "name")

def test_parsed_functions():
    parser = Parser()
    parser.from_string(sample_content["valid"])
    parsed = parser.to_dict()

    #parsed str
    test_parsed_str = str(parser)
    
    # parsed dict
    parser.from_string(test_parsed_str)
    test_parsed_dict = parser.to_dict()

    assert test_parsed_dict == parsed

##################
# test invalid   #
################## 

def test_invalid():
    parser = Parser()
    try:
        parser.from_string(sample_content["invalid"])
        assert False
    except Exception as exc:
        assert True

def test_invalid_section():
    parser = Parser()
    try:
        parser.from_string(sample_content["invalid_section"])
        assert False
    except Exception as exc:
        assert True

def test_unclosed_section():
    parser = Parser()

    with pytest.raises(Exception) as e:
        parser.from_string(sample_content["invalid_unclosed_section"])

def test_unopened_section():
    parser = Parser()

    with pytest.raises(Exception) as e:
        parser.from_string(sample_content["invalid_unopened_section"])
    

def test_no_equal():
    parser = Parser()

    with pytest.raises(Exception) as e:
        parser.from_string(sample_content["invalid_no_equal"])

def test_no_value():
    parser = Parser()

    with pytest.raises(Exception) as e:
        parser.from_string(sample_content["invalid_no_value"])

def test_no_key():
    parser = Parser()
    
    with pytest.raises(Exception) as e:
        parser.from_string(sample_content["invalid_no_key"])

def test_more_then_one_equal():
    parser = Parser()

    with pytest.raises(Exception) as e:
        parser.from_string(sample_content["invalid_more_then_one_equal"])

########################
# functions exceptions #
########################

def test_no_sections():
    parser = Parser()
    parser.from_string(sample_content["invalid_no_sections"])

    # get sections
    with pytest.raises(Exception) as e:
        parser.get_sections()

def test_wrong_section():
    parser = Parser()
    parser.from_string(sample_content["valid"])

    with pytest.raises(Exception) as e:
        parser.get_section("ownerr")

def test_no_options():
    parser = Parser()
    parser.from_string(sample_content["invalid_no_options"])
    
    with pytest.raises(Exception) as e:
        parser.get_options()

def test_wrong_option():
    parser = Parser()
    parser.from_string(sample_content["valid"])

    with pytest.raises(Exception) as e:
        parser.get_option("owner", "address")

def test_set_option_old_option():
    parser = Parser()
    parser.from_string(sample_content["valid"])
    parser.set_option("owner", "name", "Ali")

    with pytest.raises(Exception) as e:
        assert "John" == parser.get_option("owner", "name")

#####################
# test wrong values #
#####################

def test_wrong_value():
    parser = Parser()
    parser.from_string(sample_content["valid"])

    with pytest.raises(Exception) as e:
        assert parser.get_option("owner", "server") == "John"

def test_wrong_bool():
    parser = Parser()
    parser.from_string(sample_content["valid"])

    with pytest.raises(Exception) as e:
        parser.get_bool("database", "server")

def test_wrong_int():
    parser = Parser()
    parser.from_string(sample_content["valid"])

    with pytest.raises(Exception) as e:
        parser.get_int("database", "protected")

def test_wrong_float():
    parser = Parser()
    parser.from_string(sample_content["valid"])

    with pytest.raises(Exception) as e:
        parser.get_float("database", "protected")
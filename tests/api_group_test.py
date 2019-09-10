from lib.api_group import ApiGroup
from lib.errors import ApidocParseError

def test_correct():
    obj = ApiGroup("@apiGroup Articles")
    assert obj.name == "Articles"

def test_incorrect_args():
    try:
        ApiGroup("@apiGroup")
    except ApidocParseError:
        assert True
        return
    assert False

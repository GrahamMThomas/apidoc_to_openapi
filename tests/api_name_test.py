from lib.api_name import ApiName
from lib.errors import ApidocParseError

def test_correct():
    obj = ApiName("@apiName GetArticles")
    assert obj.name == "GetArticles"

def test_incorrect_args():
    try:
        ApiName("@apiName")
    except ApidocParseError:
        assert True
        return
    assert False

from apidoc_to_openapi.lib.annotations.api import Api
from apidoc_to_openapi.lib.errors import *


def test_correct():
    obj = Api("@api {get} /articles")
    assert obj is not None
    assert obj.method == "GET"
    assert obj.path == "/articles"


def test_correct_with_optional():
    obj = Api("@api {get} /articles This is the best endpoint")
    assert obj.title == "This is the best endpoint"


def test_not_enough_args():
    try:
        Api("@api {get}")
    except ApidocParseError:
        assert True
        return
    assert False


def test_bad_method():
    try:
        Api("@api {barf} /articles")
    except ApidocValidationError:
        assert True
        return
    assert False

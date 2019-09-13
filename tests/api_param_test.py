from apidoc_to_openapi.lib.annotations.api_param import ApiParam
from apidoc_to_openapi.lib.errors import ApidocParseError


def test_correct():
    obj = ApiParam('@apiParam (Query) {Number{241}="asaas","bab"} limit This is it')
    assert obj.group == "Query"
    assert obj.type == "Number"
    assert obj.type_size == "241"
    assert obj.type_allowed_values == '"asaas","bab"'
    assert obj.field == "limit"
    assert obj.description == "This is it"


def test_correct_without_group():
    obj = ApiParam('@apiParam {Number{241}="asaas","bab"} limit This is it')
    assert obj.type == "Number"
    assert obj.type_size == "241"
    assert obj.type_allowed_values == '"asaas","bab"'
    assert obj.field == "limit"
    assert obj.description == "This is it"


def test_correct_without_group_or_type():
    obj = ApiParam("@apiParam limit This is it")
    assert obj.field == "limit"
    assert obj.description == "This is it"


def test_correct_field_only():
    obj = ApiParam("@apiParam limit")
    assert obj.field == "limit"


def test_correct_field_default():
    obj = ApiParam("@apiParam limit=bobs")
    assert obj.field == "limit"
    assert obj.field_default == "bobs"
    assert not obj.field_required


def test_correct_field_default():
    obj = ApiParam("@apiParam [limit=bobs]")
    assert obj.field == "limit"
    assert obj.field_default == "bobs"
    assert obj.field_required


def test_incorrect_args():
    try:
        ApiParam("@apiParam")
    except ApidocParseError:
        assert True
        return
    assert False

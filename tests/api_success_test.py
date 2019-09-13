from apidoc_to_openapi.lib.annotations.api_success import ApiSuccess
from apidoc_to_openapi.lib.errors import ApidocParseError


def test_correct():
    obj = ApiSuccess("@apiSuccess (200) {String} api_key The keys to my kingdom")
    assert obj.group == "200"
    assert obj.type == "String"
    assert obj.field == "api_key"
    assert obj.description == "The keys to my kingdom"


def test_subclass():
    obj = ApiSuccess("@apiSuccess (200) {String} api_key.my_best_key The keys to my kingdom")
    assert obj.group == "200"
    assert obj.type == "String"
    assert obj.field == "api_key.my_best_key"
    assert obj.description == "The keys to my kingdom"


def test_group_default():
    obj = ApiSuccess("@apiSuccess {String} api_key The keys to my kingdom")
    assert obj.group == "200"
    assert obj.type == "String"
    assert obj.field == "api_key"
    assert obj.description == "The keys to my kingdom"


def test_no_type():
    obj = ApiSuccess("@apiSuccess api_key The keys to my kingdom")
    assert obj.group == "200"
    assert obj.type == None
    assert obj.field == "api_key"
    assert obj.description == "The keys to my kingdom"


def test_no_description():
    obj = ApiSuccess("@apiSuccess {String} api_key")
    assert obj.group == "200"
    assert obj.type == "String"
    assert obj.field == "api_key"
    assert obj.description == None


def test_build_parameters():
    successes = []
    successes.append(ApiSuccess("@apiSuccess (200) {Object} articles"))
    successes.append(ApiSuccess("@apiSuccess (200) {String} articles.author"))
    successes.append(ApiSuccess("@apiSuccess (200) {String} articles.created_at"))
    successes.append(ApiSuccess("@apiSuccess (200) {Object[]} articles.tanks"))
    successes.append(ApiSuccess("@apiSuccess (200) {String} articles.tanks.chassis"))
    successes.append(ApiSuccess("@apiSuccess (200) {String} articles.tanks.cannon"))
    parameters_obj = ApiSuccess.build_parameters(successes)

    # import json
    # print(json.dumps(parameters_obj, indent=2, sort_keys=False))

    assert parameters_obj == {
        "articles": {
            "type": "object",
            "properties": {
                "author": {"type": "string"},
                "created_at": {"type": "string"},
                "tanks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {"chassis": {"type": "string"}, "cannon": {"type": "string"}},
                    },
                },
            },
        }
    }


def test_build_parameters_one():
    successes = []
    successes.append(ApiSuccess("@apiSuccess (200) {Number} id"))
    parameters_obj = ApiSuccess.build_parameters(successes)

    # import json
    # print(json.dumps(parameters_obj, indent=2, sort_keys=False))

    assert parameters_obj == {"id": {"type": "number"}}


def test_incorrect_args():
    try:
        ApiSuccess("@apiSuccess")
    except ApidocParseError:
        assert True
        return
    assert False

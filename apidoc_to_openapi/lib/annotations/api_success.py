from apidoc_to_openapi.lib.annotations.apidoc_annotation import ApidocAnnotation
from apidoc_to_openapi.lib.errors import *

from apidoc_to_openapi.lib.helper_methods import getFromDict, setInDict

import re


class ApiSuccess(ApidocAnnotation):
    def __init__(self, declaration):
        self.declaration = declaration

        self.group = "200"  # Optional; Setting default because apidoc default is bad
        self.type = None  # Optional
        self.field = ""
        self.description = None  # Optional

        self.children = []

        self.parse()
        self.validate()

    def __str__(self):
        return f"ApiSuccess ({self.group}) {{{self.type}}} {self.field} : {self.description}"

    def parse(self):
        parsed = re.search(
            r"@apiSuccess ?(?:\(([0-9a-zA-Z]+)\))? ?(?:\{([a-zA-Z\]\[]+)\})? ?(?:([a-zA-Z_\.]+)) *(.+)?",
            self.declaration,
        )
        if not parsed:
            raise ApidocParseError(f"Regex failed to parse: {self.declaration}")
        self.group = parsed.group(1) or self.group
        self.type = parsed.group(2)
        self.field = parsed.group(3)
        self.description = parsed.group(4)

    def validate(self):
        types = [
            "Boolean",
            "Boolean[]",
            "Number",
            "Number[]",
            "String",
            "String[]",
            "Object",
            "Object[]",
            None,
        ]
        if self.type not in types:
            raise ApidocValidationError(f"{self.type} is not a valid type. {', '.join(types)}")

    def to_swagger(self):
        tmp = {}
        if "Object" in self.type:
            tmp = {"type": "object", "properties": {}}
        else:
            tmp = {"type": self.type.lower()}

        if "[]" in self.type:
            return {"type": "array", "items": tmp}
        return tmp

    @classmethod
    def build_parameters(cls, api_successes):
        parameters = {}
        # Slowly build the api's response parameters
        # This is to calculate nested object and arrays such as
        #
        #   @apiSuccess (200) {Object[]} articles
        #   @apiSuccess (200) {String} articles.author

        for succ in api_successes:
            nested_fields = succ.field.split(".")
            dir_path = [str(succ.group)]
            if not parameters.get(str(succ.group)):
                parameters[str(succ.group)] = {}

            # Build dictionary path to set the variable in the correct spot
            for i, field in enumerate(nested_fields[:-1]):
                nested_dirs_for_field = [field, "properties"]

                # Check to see if parent element is an array, if so, add item to the dict path
                for succ_i in api_successes:
                    if succ_i.field == ".".join(nested_fields[0 : i + 1]) and "[]" in succ_i.type:
                        nested_dirs_for_field.insert(1, "items")
                dir_path.extend(nested_dirs_for_field)

            setInDict(parameters, dir_path + [nested_fields[-1]], succ.to_swagger())

        return parameters

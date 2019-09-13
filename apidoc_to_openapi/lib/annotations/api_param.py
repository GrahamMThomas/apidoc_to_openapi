from apidoc_to_openapi.lib.annotations.apidoc_annotation import ApidocAnnotation
from apidoc_to_openapi.lib.errors import *
import re


class ApiParam(ApidocAnnotation):
    def __init__(self, declaration):
        self.declaration = declaration

        self.group = None  # Optional
        self.type = None  # Optional
        self.type_size = None  # Optional
        self.type_allowed_values = None  # Optional
        self.field = ""
        self.field_required = False
        self.field_default = None  # Optional
        self.description = None  # Optional

        self.parse()
        self.validate()

    def __str__(self):
        return f"ApiParam ({self.group}) {{{self.type}{{{self.type_size}}}={self.type_allowed_values}}} {self.field}={self.field_default} required={self.field_required} {self.description}"

    def parse(self):
        uhhhhhh_wat = re.search(
            r"@apiParam ?(?:\(([a-zA-Z]+)\))? ?(?:\{([a-zA-Z]+)(?:\{([\.0-9]+)\})?=?([\",0-9a-zA-Z]+)?\})? ?(?:([a-zA-Z]+)=?([\"a-zA-Z0-9]+)?|(?:\[([a-zA-Z]+)=?([\"a-zA-Z0-9]+)?\])) *(.+)?",
            self.declaration,
        )
        if not uhhhhhh_wat:
            raise ApidocParseError(f"Regex failed to parse: {self.declaration}")
        self.group = uhhhhhh_wat.group(1)
        self.type = uhhhhhh_wat.group(2)
        self.type_size = uhhhhhh_wat.group(3)
        self.type_allowed_values = uhhhhhh_wat.group(4)
        if uhhhhhh_wat.group(5):
            self.field = uhhhhhh_wat.group(5)
        else:
            self.field = uhhhhhh_wat.group(7)
            self.field_required = True
        self.field_default = uhhhhhh_wat.group(6) or uhhhhhh_wat.group(8)
        self.description = uhhhhhh_wat.group(9)

    def validate(self):
        types = ["array", "boolean", "integer", "number", "object", "string", None]
        if self.type and self.type.lower() not in [
            "array",
            "boolean",
            "integer",
            "number",
            "object",
            "string",
        ]:
            raise ApidocValidationError(f"{self.type} is not a valid type. {types}")

    def to_swagger(self):
        return {
            "name": self.field,
            "in": self.group.lower(),
            "description": (self.description or ""),
            "required": self.field_required,
            "schema": {"type": self.type.lower()},
        }

from lib.apidoc_annotation import ApidocAnnotation
from lib.errors import *
import re


class ApiParam(ApidocAnnotation):

    def __init__(self, declaration):
        self.declaration = declaration

        self.group = ''  # Optional
        self.type = ''  # Optional
        self.type_size = ''  # Optional
        self.type_allowed_values = ''  # Optional
        self.field = ''
        self.field_required = False
        self.field_default = ''  # Optional
        self.description = ''  # Optional

        self.parse()
        self.validate()

    def __str__(self):
        return f"ApiParam ({self.group}) {{{self.type}{{{self.type_size}}}={self.type_allowed_values}}} {self.field}={self.field_default} required={self.field_required} {self.description}"

    def parse(self):
        uhhhhhh_wat = re.search(
            r"@apiParam ?(?:\(([a-zA-Z]+)\))? ?(?:\{([a-zA-Z]+)(?:\{([\.0-9]+)\})?=?([\",0-9a-zA-Z]+)?\})? ?(?:([a-zA-Z]+)=?([\"a-zA-Z0-9]+)?|(?:\[([a-zA-Z]+)=?([\"a-zA-Z0-9]+)?\])) *(.*)?", self.declaration)
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
        pass

    def to_swagger(self):
        pass

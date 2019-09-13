from apidoc_to_openapi.lib.annotations.apidoc_annotation import ApidocAnnotation
from apidoc_to_openapi.lib.errors import *

class ApiName(ApidocAnnotation):

    def __init__(self, declaration):
        self.declaration = declaration
        self.name = ''
        self.parse(declaration.split(' ')[1:])

    def __str__(self):
        return f"ApiName - {self.name}"

    def parse(self, args):
        if not args:
            raise ApidocParseError(f"\"{self.declaration}\" - Incorrect number of arguments")
        self.name = ' '.join(args)

    def to_swagger(self):
        pass

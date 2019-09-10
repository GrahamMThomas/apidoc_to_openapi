from lib.apidoc_annotation import ApidocAnnotation
from lib.errors import *

class Api(ApidocAnnotation):

    def __init__(self, declaration):
        self.declaration = declaration
        self.method = ''
        self.path = ''
        self.title = '' # Optional
        self.parse(declaration.split(' ')[1:])
        self.validate()

    def __str__(self):
        return f"API - [{self.method}] {self.path} : {self.title}"


    def parse(self, args):
        if len(args) < 2:
            raise ApidocParseError(f"\"{self.declaration}\" - Incorrect number of arguments")
        self.method = args[0][1:-1].upper()
        self.path = args[1]
        if len(args) >= 3:
            self.title = ' '.join(args[2:])

    def validate(self):
        if self.method not in ["GET", "HEAD", "POST", "PUT", "DELETE", "TRACE", "OPTIONS", "CONNECT", "PATCH"]:
            raise ApidocValidationError(f"{self.method} is not a valid http method")

    def to_swagger(self):
        pass

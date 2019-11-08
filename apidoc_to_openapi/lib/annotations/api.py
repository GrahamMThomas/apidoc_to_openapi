from apidoc_to_openapi.lib.annotations.apidoc_annotation import ApidocAnnotation

from apidoc_to_openapi.lib.annotations.api_name import ApiName
from apidoc_to_openapi.lib.annotations.api_group import ApiGroup
from apidoc_to_openapi.lib.annotations.api_param import ApiParam
from apidoc_to_openapi.lib.annotations.api_success import ApiSuccess

from apidoc_to_openapi.lib.errors import *
from apidoc_to_openapi.lib.helper_methods import merge

import logging

logger = logging.getLogger("root")


class Api(ApidocAnnotation):
    def __init__(self, declaration):
        self.declaration = declaration
        self.method = ""
        self.path = ""
        self.title = ""  # Optional

        self.api_name = None
        self.api_group = None
        self.api_params = []
        self.api_successes = []

        self._parse(declaration.split(" ")[1:])
        self._validate()

    def construct(self, annotations):
        logger.info(f"{self.path} has {len(annotations)} recognized annotations")
        for anno in annotations:
            if isinstance(anno, ApiName):
                self.api_name = anno
            elif isinstance(anno, ApiGroup):
                self.api_group = anno
            elif isinstance(anno, ApiParam):
                self.api_params.append(anno)
            elif isinstance(anno, ApiSuccess):
                self.api_successes.append(anno)

    def to_swagger(self):
        bob = ApiSuccess.build_parameters(self.api_successes)

        large_boi = {
            "paths": {
                self.path: {
                    self.method.lower(): {
                        "summary": self.api_name.name,
                        "description": self.title,
                        "parameters": list(map(lambda x: x.to_swagger(), self.api_params)),
                        "responses": {},
                    }
                }
            }
        }

        # For each response code, give the related response successes
        for key in bob.keys():
            large_boi["paths"][self.path][self.method.lower()]["responses"][key] = {
                "description": f"Response",
                "content": {
                    "application/json": {"schema": {"type": "object", "properties": bob[key]}}
                },
            }

        return large_boi

    # Private Methods =============================

    def _parse(self, args):
        if len(args) < 2:
            raise ApidocParseError(f'"{self.declaration}" - Incorrect number of arguments')
        self.method = args[0][1:-1].upper()
        self.path = args[1]
        if len(args) >= 3:
            self.title = " ".join(args[2:])

    def _validate(self):
        if self.method not in [
            "GET",
            "HEAD",
            "POST",
            "PUT",
            "DELETE",
            "TRACE",
            "OPTIONS",
            "CONNECT",
            "PATCH",
        ]:
            raise ApidocValidationError(f"{self.method} is not a valid http method")

    def __str__(self):
        return f"API - [{self.method}] {self.path} : {self.title}"

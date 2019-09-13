import logging
import os
import re

from apidoc_to_openapi.lib.annotations import *

logger = logging.getLogger("root")
ACCEPTED_FILE_EXTENSIONS = ["py"]


def get_files_to_parse(relative_path):
    """Walks through given directory and returns all files with ending
        with an accepted file extension

    Arguments:
        relative_path {string} -- path to pull files from recursively

    Returns:
        List<String> -- list of filenames with fullpath
    """

    files = []
    filepath = os.path.realpath(relative_path)
    if os.path.isfile(filepath):
        files.append(filepath)
    else:
        for r, d, f in os.walk(filepath):
            for file in f:
                if not file.split(".")[-1] in ACCEPTED_FILE_EXTENSIONS:
                    continue
                full_file_path = os.path.join(r, file)
                files.append(os.path.join(r, full_file_path))
    return files


def find_apidoc_annotations(text):
    annotations = re.findall("@api.*", text)
    return annotations


def parse_generic_annotation(annotation):
    """Parse the name at the beginning of each annotation and build objs based on that name

    Arguments:
        annotation {string} -- apidoc compliant string

    Returns:
        ApidocAnnotation -- Returns the class matching the annotation name
    """

    class_name = "A" + annotation.split(" ")[0][2:]  # Remove the @ at the beginning and capitalize
    target_class = globals().get(class_name)
    if not target_class:
        logger.error(
            "Could not find class for %s. It is either incorrect or not supported yet.", class_name
        )
        return None

    anno_obj = target_class(annotation)
    return anno_obj

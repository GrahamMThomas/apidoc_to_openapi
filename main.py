import argparse
import glob
import os
import re
import json
import yaml
from collections import defaultdict

from lib.annotations import *

from colorama import Fore
from lib.helper_methods import merge

from lib.log import create_custom_logger

logger = create_custom_logger("root")

ACCEPTED_FILE_EXTENSIONS = ["py"]


def parse_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i")
    parser.add_argument("-o")
    parser.add_argument("--yaml", action="store_true")
    parser.set_defaults(yaml=False)
    args = parser.parse_args()
    return args


def get_files_to_parse(relative_path):
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
                logger.debug("Inspecting %s", file)
                files.append(os.path.join(r, full_file_path))
    return files


def find_apidoc_annotations(text):
    annotations = re.findall("@api.*", text)
    return annotations


def parse_generic_annotation(annotation):
    class_name = "A" + annotation.split(" ")[0][2:]
    target_class = globals().get(class_name)
    if not target_class:
        logger.error("Could not find class for %s", class_name)
        return None

    anno_obj = target_class(annotation)
    return anno_obj


def parse_apidoc_json(file_path):
    try:
        apidoc_json = open(os.path.join(file_path, "apidoc.json"), "r").read()
        apidoc_conf = json.loads(apidoc_json)
        return apidoc_conf
    except FileNotFoundError:
        logger.error("Could not locate apidoc.json in %s", file_path)
        exit(1)
    except json.decoder.JSONDecodeError:
        logger.error("apidoc.json Invalid JSON!")
        exit(1)


def build_info_section(apidoc_conf):
    info_section = {}
    info_section["title"] = apidoc_conf.get("title") or apidoc_conf.get("name")
    info_section["version"] = apidoc_conf.get("version", "0.0.0")
    info_section["description"] = apidoc_conf.get("description")
    return info_section


def main():
    logger.info(f"{Fore.GREEN}Hello{Fore.RESET}")
    args = parse_command_line_args()
    swagger = {"openapi": "3.0.0"}

    apidoc_conf = parse_apidoc_json(args.i)
    swagger["info"] = build_info_section(apidoc_conf)

    annotations_objs = []
    for filepath in get_files_to_parse(args.i):
        file_contents = open(filepath, "r").read()
        annotations = find_apidoc_annotations(file_contents)

        for anno in annotations:
            annotations_objs.append(parse_generic_annotation(anno))
    # Take every
    api_indices = [i for i, v in enumerate(annotations_objs) if isinstance(v, Api)]
    for i, v in enumerate(api_indices):
        annotations_objs[v].construct(
            annotations_objs[v : (api_indices[i + 1] if len(api_indices) > i + 1 else None)]
        )

    for i in api_indices:
        merge(swagger, annotations_objs[i].to_swagger())

    if args.yaml:
        print("\n================YAML=================")
        print(yaml.dump(swagger, indent=2, sort_keys=False))
        print("=====================================\n")
    else:
        print("\n================JSON=================")
        print(json.dumps(swagger, indent=2))
        print("=====================================\n")


if __name__ == "__main__":
    main()

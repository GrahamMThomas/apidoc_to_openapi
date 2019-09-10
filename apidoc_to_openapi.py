import argparse
import glob
import os
import re

from lib.api import Api
from lib.api_name import ApiName
from lib.api_group import ApiGroup
from lib.api_param import ApiParam

from colorama import Fore

from lib.log import create_custom_logger

logger = create_custom_logger('root')

ACCEPTED_FILE_EXTENSIONS = ['py']

def parse_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i')
    parser.add_argument('-o')
    args = parser.parse_args()
    return args

def get_files_to_parse(relative_path):
    files = []
    filepath = os.path.realpath(relative_path)
    print(filepath)
    if os.path.isfile(filepath):
        files.append(filepath)
    else:
        for r, d, f in os.walk(filepath):
            for file in f:
                if not file.split('.')[-1] in ACCEPTED_FILE_EXTENSIONS:
                    continue
                full_file_path = os.path.join(r, file)
                logger.debug("Inspecting %s", file)
                files.append(os.path.join(r, full_file_path))
    return files

def find_apidoc_annotations(text):
    annotations = re.findall("@api.*", text)
    return annotations

def parse_generic_annotation(annotation):
    class_name = 'A'+annotation.split(' ')[0][2:]
    target_class = globals().get(class_name)
    if not target_class:
        logger.error("Could not find class for %s", class_name)
        return None

    anno_obj = target_class(annotation)
    print(anno_obj)
    return anno_obj



def main():
    logger.info(f"{Fore.GREEN}Hello{Fore.RESET}")
    args=parse_command_line_args()

    for filepath in get_files_to_parse(args.i):
        file_contents = open(filepath, 'r').read()
        annotations = find_apidoc_annotations(file_contents)
        for anno in annotations:
            parse_generic_annotation(anno)
    # print(os.getcwd())




if __name__ == "__main__":
    main()

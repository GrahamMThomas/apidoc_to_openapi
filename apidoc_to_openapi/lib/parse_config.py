import json
import os

import logging

logger = logging.getLogger("root")


def parse_apidoc_json(file_path):
    """Parses the required apidoc.json file at the root of the user specified directory

    Returns:
        dict -- apidoc.json file after being json parsed
    """

    try:
        apidoc_json = open(os.path.join(file_path, "apidoc.json"), "r").read()
        apidoc_conf = json.loads(apidoc_json)
        return apidoc_conf
    except FileNotFoundError:
        logger.error("Could not locate apidoc.json in %s", (file_path))
        exit(1)
    except json.decoder.JSONDecodeError:
        logger.error("apidoc.json Invalid JSON!")
        exit(1)


def build_info_section(apidoc_conf):
    """Converts apidoc.json to swagger configuration

    Arguments:
        apidoc_conf {dict} -- apidoc.json converted to a dictionary

    Returns:
        dict -- dictionary matching the require infomation section for swagger
    """
    info_section = {}
    info_section["title"] = apidoc_conf.get("title") or apidoc_conf.get("name")
    info_section["version"] = apidoc_conf.get("version", "0.0.0")
    info_section["description"] = apidoc_conf.get("description")
    return info_section

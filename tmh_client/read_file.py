"""Module to read date from files."""
# stdlib
import os
import json
import logging


def file_exists(full_path: str) -> bool:
    """
    Checks if a file in a given directory exists.

    :param full_path: string, | full path of folder where file is stored
                              | with suffix e.g. .csv, .json
    :return: boolean, result if file existing check
    """
    return os.path.isfile(full_path)


def json_to_dict(path: str,
                 file_name: str) -> dict:
    """
    Read in a .json file and save the data in a dictionary if
    the file exists.

    :param path: string, path of folder where .json file is saved
    :param file_name: string, | name of .json file. Has to have
                              | the extension .json in the variable
    :return: dict data frame, data from .json file
    """
    full_path: str = os.path.join(path, file_name)

    if file_exists(full_path):
        with open(full_path, encoding="utf-8") as json_file:
            data: dict = json.load(json_file)
        return data

    logging.warning("%s not found", full_path)
    raise OSError(f"{full_path} not found")

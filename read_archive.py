#!/usr/bin/env python3

from pathlib import Path
from configparser import ConfigParser
import argparse
import requests
import json
import os


def read_archive(directory):
    '''
    read config files
    '''
    archive = Path(directory).glob('**/index.cfg')
    print(archive)

    for idx, exp_path in enumerate(archive):

        if idx >= 10:
            break
        
        config = ConfigParser()
        config.read(exp_path)
        config_dict = {s: dict(config.items(s))for s in config.sections()}

        print(f'\nThe experiment was performed on: "{config_dict["meta"]["date"]}"')

        number_of_params = len(config_dict['info'].items())
        print(f'There are {number_of_params} parameters')
        for key, value in config_dict['info'].items():
            print(f' "{key}": "{value}"')

        files = config_dict["meta"]['files']
        files_list = files.split()

        number_of_blobs = len(config_dict['fileinfo'].items())
        print(f'There are {number_of_blobs} blobs')

        dir_path = os.path.dirname(exp_path)

        for file in files_list:
            file_path = os.path.join(dir_path, file)
            if not os.path.isfile(file_path):
                raise FileNotFoundError(file)
            print(f' Name: "{config_dict["fileinfo"][file]}", File: "{file}"')

# parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("--archive_dir", "-a", required=True,
                help="archive directory containing 'index.cfg' files")
args = ap.parse_args()
archive_dir = args.archive_dir

# calling the function
read_archive(archive_dir)

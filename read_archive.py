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

        if idx < 10:
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

            dir_files = []
            for dirpath, _, filenames in os.walk(directory):
                for f in filenames:
                    if not f.startswith('.') and f != 'index.cfg':
                        dir_files.append(f)
            
            for file in files_list:
                if file in dir_files:
                    print(f' Name: "{config_dict["fileinfo"][file]}", File: "{file}"')
                else:
                    raise FileNotFoundError(file)
        else:
            break

# parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("--archive", "-a", required=True,
                help="archive directory containing 'index.cfg' files")
args = vars(ap.parse_args())

# calling the function
read_archive(args['archive'])

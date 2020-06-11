#!/usr/bin/env python3

import datetime
from pathlib import Path
from configparser import ConfigParser
import argparse
import json
import requests
import os

class RemoveExperimentException(Exception):
    '''
    Remove experiment error
    '''
    def __init__(self, message):
        super(RemoveExperimentException, self).__init__()
        self.message = message


def get_page(demo_id):
    '''
    Get the pages
    '''
    params = {'demo_id': demo_id}
    response = requests.get('http://127.0.0.1/api/archive/get_page', params=params).json()
    return response


def delete_experiment(experiment_id):
    '''
    Remove an experiment
    '''
    params = {'experiment_id': experiment_id}
    response = requests.delete('http://127.0.0.1/api/archive/delete_experiment', params=params).json()
    if response['status'] == 'OK':
        print(response)
    else:
        raise RemoveExperimentException("data not found")


def read_archive(directory):
    '''
    Read config files
    '''
    archive = Path(directory).glob('**/index.cfg')

    for idx, exp_path in enumerate(archive):
        
        config = ConfigParser()
        config.read(exp_path)
        config_dict = {s: dict(config.items(s))for s in config.sections()}

        parameters = config_dict['info']
        date = config_dict['meta']['date']

        blobs = []
        for key, value in config_dict['fileinfo'].items():
            name = value
            file = key
            dir_path = os.path.dirname(exp_path)
            file_path = os.path.join(dir_path, key)
            if not os.path.isfile(file_path):
                raise FileNotFoundError(file)
            blobs.append({name: file_path, 'thumbnail': file_path})

        yield blobs, parameters, date


def add_experiment(demo_id, blobs, parameters):
    '''
    Add experiment to the archive
    '''
    params={
        'demo_id': demo_id,
        'blobs': json.dumps(blobs),
        'parameters': json.dumps(parameters)
    }
    response = requests.post('http://127.0.0.1/api/archive/add_experiment', params=params).json()
    try:
        if response['status']=='OK':
            print(response)
        else:
            print(f'Error (not OK): "{response}"')
    except Exception as e:
        print(e)
    return response


def update_experiment_date(experiment_id, date):
    '''
    Update the date of experiment
    '''
    params={
        'experiment_id': experiment_id,
        'date': date,
        'date_format': '%Y/%m/%d %H:%M'
    }
    response = requests.post('http://127.0.0.1/api/archive/update_experiment_date', params=params).json()
    print(response)


# parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("--demo_id", "-id", required=True,
                type=int, help="demo id required")
ap.add_argument("--archive_dir", "-a", required=True,
                help="archive directory containing 'index.cfg' files")
args = ap.parse_args()
demo_id = args.demo_id
archive_dir = args.archive_dir


# clear the archive
nb_pages = get_page(demo_id)['meta']['number_of_pages']
total_exps = get_page(demo_id)['meta']['number_of_experiments']

print(f"Experiments Deleting: {total_exps}")

for i in range(nb_pages):
    page = get_page(demo_id)
    for experiment in page['experiments']:
        print(experiment['id'])
        delete_experiment(experiment['id'])

print("\nDone Deleting \n")


#Porting archives

print("\nPorting archive\n")

for count, (blobs, parameters, date) in enumerate(read_archive(archive_dir), 1):
    response = add_experiment(demo_id, blobs, parameters)

    update_experiment_date(response['id_experiment'], date)

    if count % 100 == 0:
        print(f"\n\nExperiments Done: {count}")
        now = datetime.date.today()
        print(f"Date: {now.strftime('%Y-%m-%d')}")
        print("\n")

print("\nDone Porting\n")

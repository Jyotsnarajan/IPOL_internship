#!/usr/bin/env python3

from configparser import ConfigParser
import datetime as dt
import datetime
import sqlite3
import os.path
import argparse
import json
import requests

class RemoveExperimentException(Exception):
    '''
    Remove experiment error
    '''
    def __init__(self, message):
        super(RemoveExperimentException, self).__init__()
        self.message = message

def get_data(demo_id):
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
    
    if response['status']!='OK':
        raise RemoveExperimentException("Data Not Found")

def read_from_db():

    BASE_DIR = os.path.dirname(os.path.abspath(os.path.join(archive_dir, 'index.db')))
    db_path = os.path.join(BASE_DIR, 'index.db')

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT key, date FROM buckets WHERE public = 1 AND date > ? ', (last_date,))
    data = c.fetchall()

    for key, date in data:
        dir_path = os.path.join(archive_dir, key[:2], key[2:])
        archive = os.path.join(dir_path, 'index.cfg')
        config = ConfigParser()
        config.read(archive)
        config_dict = {s: dict(config.items(s))for s in config.sections()}
        parameters = config_dict['info']

        blobs = []
        for key, value in config_dict['fileinfo'].items():
            name = value
            file = key
            file_path = os.path.join(dir_path, file)
            if not os.path.isfile(file_path):
                raise FileNotFoundError(file)
            blobs.append({name: file_path, 'thumbnail': file_path})

        yield blobs, parameters, date


def get_page(demo_id, page):
    '''
    Get the page
    '''
    params = {'demo_id': demo_id,
            'page': page}
    response = requests.get('http://127.0.0.1/api/archive/get_page', params=params).json()
    return response


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
    
    assert response ['status'] == 'OK'
    return response

def update_experiment_date(experiment_id, date):
    '''
    Update the date of experiment
    '''
    params={
        'experiment_id': experiment_id,
        'date': date,
        'date_format': '%Y-%m-%d %H:%M'
    }
    response = requests.post('http://127.0.0.1/api/archive/update_experiment_date', params=params).json()

    assert response ['status'] == 'OK'
    return response

# parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("--demo_id", "-id", required=True,
                type=int, help="demo id required")
ap.add_argument("--archive_dir", "-a", required=True,
                help="archive directory containing 'index.cfg' files")
ap.add_argument("-r", '--remove', help="Remove Demo", action="store_true")
args = ap.parse_args()
demo_id = args.demo_id
archive_dir = args.archive_dir

# clear the archive
if args.remove:
    nb_pages = get_data(demo_id)['meta']['number_of_pages']
    total_exps = get_data(demo_id)['meta']['number_of_experiments']

    print(f"Experiments Deleting: {total_exps}\n")

    for i in range(nb_pages):
        page = get_data(demo_id)
        for experiment in page['experiments']:
            delete_experiment(experiment['id'])

    print(f"Done Deleting: {total_exps}")

#last archived date
last_page_info = get_page(demo_id, 0)
experiments = last_page_info['experiments']
res = not bool(experiments)
if res!=True: 
    last_date = experiments[-1]['date']
    last_date = dt.datetime.strptime(last_date, '%Y-%m-%d %H:%M:%S')
    last_date = last_date.strftime('%Y/%m/%d %H:%M:')
    print(f' last date: {last_date}')

else:
    last_date = '1880/08/08 05:42'


#Porting Archive
print("\nPorting archive\n")
for count, (blobs, parameters, date) in enumerate(read_from_db(), 1):
    
    date = dt.datetime.strptime(date, '%Y/%m/%d %H:%M')
    new_date = date.strftime('%Y-%m-%d %H:%M')

    response = add_experiment(demo_id, blobs, parameters)
    update_experiment_date(response['id_experiment'], new_date)
        
    if count % 100 == 0:
        print(response)
        print(f"\nDemo: {demo_id}")
        print(f"Experiments Added: {count}")
        now = datetime.date.today()
        print(f"Date: {now.strftime('%Y-%m-%d')}")
        print("\n")

print("\nDone Porting\n")

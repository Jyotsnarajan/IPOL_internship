#!/usr/bin/env python3

from pathlib import Path
from urllib.request import urlopen
from configparser import ConfigParser
import argparse
import json
import os
import requests

def get_blobs(demo_id):
    '''
    get all the blobs
    '''
    params = {'demo_id': demo_id}
    response = requests.get('http://integration.ipol.im/api/blobs/get_blobs', params=params).json()
    return response

def remove_blob_from_demo(demo_id, blob_set, pos_set):
    '''
    remove all blobs from demo
    '''
    params = {'demo_id': demo_id,
            'pos_set': pos_set,
            'blob_set': blob_set}
    response = requests.delete('http://integration.ipol.im/api/blobs/remove_blob_from_demo', params=params).json()
    print(response)

    assert response['status'] == 'OK'

def add_blob_to_demo(path, demo_id, title, credit):
    '''
    add all blobs to demo
    '''
    params = {
            'demo_id': demo_id,
            'title': title,
            'credit': credit
    }
    files = {'blob': urlopen('file:///' + path)}
    response = requests.post('http://integration.ipol.im/api/blobs/add_blob_to_demo', params=params, files=files).json()
    print(response)

    assert response['status'] == 'OK'

def gen_input(directory):
    """
    Config from input directory
    """
    conf = ConfigParser()
    conf.read(os.path.join(directory, 'index.cfg'))
    for name, blob in [(s, dict(conf.items(s)))for s in conf.sections()]:
        path = os.path.join(directory, blob.get('files', ''))
        title = blob['title']
        credit = blob['credit']
        yield path, title, credit

                          
# parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("--demo_id", "-id", required=True,
                type=int, help="demo id required")
ap.add_argument("--blobs", "-b", required=True,
                 help="blobs directory that contains index.cfg file")              
args = ap.parse_args()
demo_id = args.demo_id
blobs = args.blobs

# deleting all the blobs
demo_blobs = get_blobs(demo_id)
keys = demo_blobs.keys()
sets = demo_blobs['sets']

print("Deleting Blobs")

for set in sets:
    for key in set['blobs'].keys():
        blob_set = set['name']
        pos_set = key
        remove_blob_from_demo(demo_id, blob_set , pos_set)

#adding all the blobs

metadata = gen_input(blobs)
print("\n")
print(f"Adding blobs, metadata={metadata}\n")

for count, (path, title, credit) in enumerate(metadata, 1):
    print(count, path, title, credit)
    add_blob_to_demo(path, demo_id, title, credit)
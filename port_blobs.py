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
    response = requests.get('http://localhost/api/blobs/get_blobs', params=params).json()
    #print(response)
    return response

def remove_blob_from_demo(demo_id, blob_set, pos_set):
    '''
    remove all blobs from demo
    '''
    params = {'demo_id': demo_id,
            'pos_set': pos_set,
            'blob_set': blob_set}
    response = requests.delete('http://localhost/api/blobs/remove_blob_from_demo', params=params).json()
    print(response)


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
    response = requests.post('http://localhost/api/blobs/add_blob_to_demo', params=params, files=files).json()
    print(response)


def gen_input(directory):
    """
    Config from input directory
    """
    conf = ConfigParser()
    conf.read(os.path.join(directory, 'index.cfg'))
    for name, blob in [(s, dict(conf.items(s)))for s in conf.sections()]:
        #print(blob)
        path = os.path.join(directory, blob.get('files', ''))
        file = blob['files']
        title = blob['title']
        credit = blob['credit']
        add_blob_to_demo(path, demo_id, title, credit)
        
              
# parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("--demo_id", "-id", required=True,
                type=int, help="demo id required")
ap.add_argument("--blobs", "-b", required=True,
                 help="blobs directory that contains index.cfg file")              
args = ap.parse_args()
demo_id = args.demo_id
blobs = args.blobs

#calling the function to read the index.cfg files 
gen_input(blobs)

# deleting all the blobs
demo_blobs = get_blobs(demo_id)
keys = demo_blobs.keys()
sets = demo_blobs['sets']
for set in sets:
    print(set['name'])
    for key in set['blobs'].keys():
        remove_blob_from_demo(demo_id, set['name'] , key)
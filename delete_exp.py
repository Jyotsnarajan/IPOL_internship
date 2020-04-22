#!/usr/bin/env python3

import requests
import logging
import argparse
import json

def get_info(demo_id):
	'''
    Get info from archive
    '''
	params = {'demo_id': demo_id}
	r = requests.get('http://localhost/api/archive/get_page', params=params)
	response = r.json()
	return response

def get_page(demo_id, page):
    '''
    Get the pages
    '''
    params = {'demo_id': demo_id}
    r1 = requests.get('http://localhost/api/archive/get_page', params=params)
    response1 = r1.json()
    return response1
    
def delete_experiment(experiment_id):
    '''
    Remove an experiment
    '''
    params = {'experiment_id': experiment_id}
    r2 = requests.delete('http://localhost/api/archive/delete_experiment', params=params)
    response2 = r2.json()
    print(response2)

#parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("--demoid", "-id", required = True, help = "demo id required")
args = vars(ap.parse_args())

#clear the archive
nb_pages = get_info(args['demoid'])['meta']['number_of_pages']
per_page_exp = get_info(args['demoid'])['meta']['number_of_experiments_in_a_page']
   
for i in range(nb_pages):
	page = get_page(args['demoid'], i)
	for experiment in page['experiments']:
		print(experiment['id'])
		delete_experiment(experiment['id'])

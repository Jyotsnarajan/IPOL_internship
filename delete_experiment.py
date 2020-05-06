#!/usr/bin/env python3

import requests
import argparse
import json

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
	if response2['status']=='OK':
		print(response2)
	else:
		raise RemoveExperimentException("data not found")
			
		
#parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("--demo_id", "-id", required = True, type=int, help = "demo id required")
args = ap.parse_args()
demo_id = args.demo_id

#clear the archive
nb_pages = get_page(demo_id)['meta']['number_of_pages']

for i in range(nb_pages):
	page = get_page(demo_id)
	for experiment in page['experiments']:
		print(experiment['id'])
		delete_experiment(experiment['id'])

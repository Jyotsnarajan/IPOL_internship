#!/usr/bin/env python3

import requests
import logging
import argparse
import json
import sys

get_page_url = 'http://localhost/api/archive/get_page'
delete_experiment_url = 'http://localhost/api/archive/delete_experiment'

#parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("--demoid", "-id", required = True, help = "demo id required")
args = vars(ap.parse_args())
print(args)

def get_page(demo_id, page):
	 params = {
	 'demo_id': demo_id,
	 }
	 r = requests.get(get_page_url, params=params)
	 response = r.json()
	 status = response['stauts']
	 print(status)
	 
#checking if the archive is empty
	 
	 nb_pages = response['meta']['number_of_pages']
	 
	 i = 1
	 while(i <= nb_pages):
		 get_page(args['demoid'], i)
		 if response['status']!='OK':
			 logging.error("page cannot be accessed")
			 sys.exit(-1)
		 else:
			 print(f'pages to be deleted: "{response}"')
			 delete_experiment(experiment_id)
			 print("all the experiments of current page are deleted")
			 i += 1
			 			 			 		 
def delete_experiment(experiment_id):
    params = {
        'experiment_id': experiment_id
    }
    r1 = requests.post(delete_experiment_url, params=params)
    response1 = r1.json()

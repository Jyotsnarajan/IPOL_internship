#!/usr/bin/env python3
from urllib.request import urlopen
import requests
import json
import argparse

url = 'http://localhost/api/archive/add_experiment'

#parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("--image", "-i", required = True, help = "Path to input image")
ap.add_argument("--image1", "-i1", required = True, help = "Path to input image")
args = vars(ap.parse_args())

#add an experiment to the archive
def add_experiment(demo_id, blobs, parameters):

	params = {
		'demo_id': demo_id,
		'blobs': json.dumps(blobs),
		'parameters': json.dumps(parameters)
	}
	
#request the post service
	r = requests.post(url, params=params)
	
#print the response
	print(r.status_code)
	response = r.json()
	if response['status']!='OK':
		raise CustomError("An error occurred")
	else:
		print(response)
		
#calling the experiment
add_experiment(77777000049, [{"input image": args['image']}, {"votes": args['image1']}], {"trend": 100})
    
    
    
    
    
    


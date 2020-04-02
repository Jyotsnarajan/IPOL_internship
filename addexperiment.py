#!/usr/bin/env python3
from urllib.request import urlopen
import requests
import json
import argparse
from PIL import Image

url = 'http://localhost/api/archive/add_experiment'

#parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("--cat", "-i", required = True, help = "Path to input image")
ap.add_argument("--votes", "-i1", required = True, help = "Path to input image")
ap.add_argument("--catthumb", "-it", required = True, help = "Path to input image")
ap.add_argument("--votesthumb", "-it1", required = True, help = "Path to input image")
args = vars(ap.parse_args())

# creating thumbnails  
image = Image.open(args['cat'])
image1 = Image.open(args['votes'])
MAX_SIZE = (100, 100)
image.thumbnail(MAX_SIZE)
image1.thumbnail(MAX_SIZE) 
image.save(args['catthumb'])
image1.save(args['votesthumb'])

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
add_experiment(77777000049, [{"input image": args['cat'], "thumbnail": args['catthumb']}, {"votes": args['votes'], "thumbnail": args['votesthumb']}], {"trend": 100})
    
    
    
    
    
    


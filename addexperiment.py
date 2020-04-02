#!/usr/bin/env python3
from urllib.request import urlopen
import requests
import json
import argparse
from PIL import Image
import os

url = 'http://localhost/api/archive/add_experiment'
path = '/home/jyotsna/Downloads/'

#parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("--cat", "-i", required = True, help = "Path to input image")
ap.add_argument("--votes", "-i1", required = True, help = "Path to input image")
args = vars(ap.parse_args())

# creating thumbnails
MAX_SIZE = (100, 100)
for image in args.values():
	filename, ext = os.path.splitext(image)
	file = Image.open(image)
	file.thumbnail(MAX_SIZE)
	file.save(filename + '_thumbnail.png')

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
add_experiment(77777000049, [{"input image": args['cat'], "thumbnail": os.path.join(path, "cat_thumbnail.png")}, {"votes": args['votes'], "thumbnail": os.path.join(path, "votes_thumbnail.png")}], {"trend": 100})
    
    
    
    
    
    


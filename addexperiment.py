#!/usr/bin/env python3
from urllib.request import urlopen
from PIL import Image
import argparse
import requests
import json
import os

url = 'http://localhost/api/archive/add_experiment'
path = '/home/jyotsna/Downloads/'
path1 = os.path.join(path, "cat_thumbnail.png")
path2 = os.path.join(path, "votes_thumbnail.png")

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
	try:
		if response['status'] == 'OK':
			print(response)
		else:
			print(f'Error (not OK): "{response}"')
	except Exception as e:
		print(e)

#blobs parameter to be passed
blobs = [{"cat": args['cat'], "thumbnail": path1}, {"votes": args['votes'], "thumbnail": path2}]

#calling the experiment
add_experiment(77777000049, blobs, {"trend": 100})
    
    
    
    
    
    


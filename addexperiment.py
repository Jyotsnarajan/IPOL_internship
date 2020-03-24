#!/usr/bin/env python3
from urllib.request import urlopen
import requests
import json
import sys
import os

url = 'http://localhost/api/archive/add_experiment'

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))
path = sys.argv[1]
if os.path.exists(path):
    print("File exist")

# Get filename
print("filename : " + path.split("/")[-1])

#add an experiment to the archive
def add_experiment(self, demo_id, blobs, parameters, execution=None):
	files = {'blob': urlopen('file:///' + path)}
	params = {
		'demo_id': demo_id,
		'blobs': json.dumps(blobs),
		'parameters': json.dumps(parameters)
	}
	r = requests.post(url, params=params, files=files)
	print(r.json())
add_experiment(None, 49, [{"blob1": "Home/Downloads/cat.png"}], {"trend": 100}, None)

    


    
    
    
    
    
    
    
    


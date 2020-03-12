#!/usr/bin/env python3
import requests
import json

# Request the ping service
r = requests.get('http://localhost/api/blobs/ping')
a = r.json()

# Print the status
status = a['status']
if status == 'OK':
	print('I received a pong')
else:
	print(f'Error: "{status}"')

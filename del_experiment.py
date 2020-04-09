#!/usr/bin/env python3

import requests
import logging
import argparse
import json
import sys

# [Miguel] Put the functions here

# [Miguel] Pass directly the URLs to the functions.
get_page_url = 'http://localhost/api/archive/get_page'
delete_experiment_url = 'http://localhost/api/archive/delete_experiment'

#parse the arguments
'''
[Miguel] It's better if you pass the demo_id as an argument, and not as an option.
For example, you can do it as in our demo_copy.py tool

parser = argparse.ArgumentParser()
parser.add_argument("demo_id", type=int, help="identifier of the demo to be copied")
parser.add_argument("-i", '--integration', help="Use integration environment", action="store_true")
args = parser.parse_args()

Then, obtain the variables from the parser:
args_demo_id = args.demo_id
if args.integration:
    origin_host = "integration.ipol.im"
else:
    origin_host = "ipolcore.ipol.im"

I'd avoid the vars(.) thing

'''
ap = argparse.ArgumentParser()
ap.add_argument("--demoid", "-id", required = True, help = "demo id required")
args = vars(ap.parse_args())
print(args)

# [Miguel] Put the functions before

def get_page(demo_id, page):
    '''
    [Miguel] Add the function description here
    '''
	 params = {'demo_id': demo_id}
     # [Miguel] Pass directly the URLs to the functions.
	 r = requests.get(get_page_url, params=params)
	 response = r.json()
	 print(response)
	 
#clering the archive	 
	 nb_pages = response['meta']['number_of_pages']
     
     '''
     [Miguel]
     Be careful, because you're obtaining the number of pages and then
     removing experiments. The problem is that as you remove experiments,
     the number of pages will decrease!
     
     The correct way to do it is to obtain always the first page, then
     move all the experiments, and iterate again (until there are no experiments).
     If you remove all the experiments in the first page, the second time there
     will still exist a first page, but it'll contain different experiments.
     
     It's like removing the first page of a book. Even if you do so, still there will be
     a page that will be the first (the one that before was the second).
     '''
	 
	 i = 1
	 while(i <= nb_pages):
		 get_page(args['demoid'], i) # [Miguel] I don't get this. Are you calling this same function?
		 if response['status'] != 'OK':
			 logging.error("page cannot be accessed")
			 sys.exit(-1)
		 #else: # [Miguel] You can remove the else and go on normally
         print(f'pages to be deleted: "{response}"')
         
         '''
         [Miguel] I guess the code is not finished in this part.
         experiment_id is not defined yet.
         So, it should iterate throughout all the experiments in the page and
         remove all of them. 
         '''
         delete_experiment(experiment_id)
         print("all the experiments of current page are deleted")
         i += 1
			 			 			 		 
def delete_experiment(experiment_id):
    '''
    [Miguel] Add the function description here
    '''
    params = {'experiment_id': experiment_id}
    r1 = requests.post(delete_experiment_url, params=params)
    response1 = r1.json()
    
    '''
    [Miguel] Looks good.
    You just need to check the response and log the error if anything's went wrong.
    '''

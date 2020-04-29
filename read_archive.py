#!/usr/bin/env python3

from pathlib import Path
from configparser import ConfigParser
import argparse
import requests
import json

def read_archive(directory):
	'''
	read config files
	'''
	archive = Path(directory).glob('**/index.cfg')
	print(archive)
	
	for idx, exp_path in enumerate(archive):
		
		if idx<10:
			config = ConfigParser()
			config.read(exp_path)
			config_dict = {s: dict(config.items(s))for s in config.sections()}
			
			print(config_dict['info'])
			print(config_dict['fileinfo'])		    		  		    
		else:
			break														

#parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("--archive", "-a", required = True, help = "archive directory containing 'index.cfg' files")
args = vars(ap.parse_args())

#calling the function
read_archive(args['archive'])

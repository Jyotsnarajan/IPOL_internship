#!/usr/bin/env python3

import argparse
import os

# parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("add_noise", type=str, default="True")
ap.add_argument("sigma", type=int)
ap.add_argument("noisemodel", type=str)
args = ap.parse_args()

#string to bool
args.add_noise = args.add_noise.lower() == 'true'

noise = 1 if args.add_noise else 0

noisearg = str.lower(args.noisemodel) + ':' + str(args.sigma)
darg = '-D' + str(4*float(args.sigma))

if noise == 0:		
	p1 = f'tvdenoise -n {noisearg} input_0.png denoised.png'
	os.system(p1)
	
	p2 = f'imdiff {darg} input_0.png denoised.png diff.png'
	os.system(p2)

else:
	p1 = f'imnoise {noisearg} input_0.png noisy.png'
	os.system(p1)
	
	p2 = f'tvdenoise -n {noisearg} noisy.png denoised.png'
	os.system(p2)
	
	p3 = 'imdiff -mrmse input_0.png noisy.png'
	os.system(p3)

	p4 = 'imdiff -mrmse input_0.png denoised.png'
	os.system(p4)

	p5 = f'imdiff {darg} input_0.png denoised.png diff.png'
	os.system(p5)

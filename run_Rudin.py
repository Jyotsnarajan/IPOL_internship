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
add_noise = args.add_noise.lower() == 'true'

add_noise = 1 if args.add_noise else 0

noisearg = str.lower(args.noisemodel) + ':' + str(args.sigma)
darg = '-D' + str(4*float(args.sigma))

if add_noise == 0:		
	p1 = f'tvdenoise -n {noisearg} input_0.png denoised.png'
	if os.system(p1)!= 0: exit(-1)
	
	p2 = f'imdiff {darg} input_0.png denoised.png diff.png'
	if os.system(p2)!= 0: exit(-1)

else:
	p1 = f'imnoise {noisearg} input_0.png noisy.png'
	if os.system(p1)!= 0: exit(-1)
	
	p2 = f'tvdenoise -n {noisearg} noisy.png denoised.png'
	if os.system(p2)!= 0: exit(-1)
	
	p3 = 'imdiff -mrmse input_0.png noisy.png'
	if os.system(p3)!= 0: exit(-1)

	p4 = 'imdiff -mrmse input_0.png denoised.png'
	if os.system(p4)!= 0: exit(-1)

	p5 = f'imdiff {darg} input_0.png denoised.png diff.png'
	if os.system(p5)!= 0: exit(-1)

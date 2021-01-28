#!/usr/bin/env python3

import argparse
import os

# parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("add_noise", type=str, default="True")
ap.add_argument("sigma", type=int)
ap.add_argument("iteration", type=int)
args = ap.parse_args()


#string to bool
add_noise = args.add_noise.lower() == 'true'

add_noise = 1 if add_noise else 0

darg = '-D' + str(4*float(args.sigma))
noisearg = 'gaussian' + ':' + str(args.sigma)

if add_noise == 0:	
	p1 = f'denoiseSPLE input_0.png {args.sigma} {args.iteration} denoised.png'
	if os.system(p1)!= 0: exit(-1)

	p2 = f'imdiff {darg} input_0.png denoised.png diff.png'
	if os.system(p2)!= 0: exit(-1)

else:
	p1 = f'imnoise {noisearg} input_0.png noisy.png'
	if os.system(p1)!= 0: exit(-1)
	
	p2 = f'denoiseSPLE input_0.png {args.sigma} {args.iteration} denoised.png'
	if os.system(p2)!= 0: exit(-1)

	p3 = f'imdiff -mrmse input_0.png denoised.png diff.png'
	if os.system(p3)!= 0: exit(-1)

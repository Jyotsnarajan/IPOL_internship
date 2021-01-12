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
args.add_noise = args.add_noise.lower() == 'true'

noise = 1 if args.add_noise else 0

darg = '-D' + str(4*float(args.sigma))
noisearg = 'gaussian' + ':' + str(args.sigma)

if noise == 0:	
	p1 = f'denoiseSPLE input_0.png {args.sigma} {args.iteration} denoised.png'
	os.system(p1)

	p2 = f'imdiff {darg} input_0.png denoised.png diff.png'
	os.system(p2)

else:
	p1 = f'imnoise {noisearg} input_0.png noisy.png'
	os.system(p1)
	
	p2 = f'denoiseSPLE input_0.png {args.sigma} {args.iteration} denoised.png'
	os.system(p2)

	p3 = f'imdiff -mrmse input_0.png denoised.png diff.png'
	os.system(p3)

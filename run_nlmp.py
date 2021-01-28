#!/usr/bin/env python3

import argparse
import os

# parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("add_noise", type=str, default="True")
ap.add_argument("sigma", type=int)
args = ap.parse_args()


#string to bool
add_noise = args.add_noise.lower() == 'true'

add_noise = 1 if args.add_noise else 0

#noisy and denoised images	
p1 = f'NLMeansP input_0.png {args.sigma} {add_noise} input_1.png output_1.png'
if os.system(p1)!= 0:
	exit(-1)

#compute image differences
p2 = f'img_diff_ipol input_0.png output_1.png {args.sigma} output_2.png'
if os.system(p2)!= 0:
	exit(-1)

#estimate MSE and PSNR
p3 = 'img_mse_ipol input_0.png output_1.png'
if os.system(p3)!= 0:
	exit(-1)


#!/usr/bin/env python3

import argparse
import os
import sys

# parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("add_noise", type=str, default="True")
ap.add_argument("sigma", type=int)
args = ap.parse_args()


#string to bool
args.add_noise = args.add_noise.lower() == 'true'

noise = 1 if args.add_noise else 0

#noisy and denoised images	
p1 = f'NLMeansP input_0.png {args.sigma} {noise} input_1.png output_1.png'
val1 = os.system(p1)

#compute image differences
p2 = f'img_diff_ipol input_0.png output_1.png {args.sigma} output_2.png'
val2 = os.system(p2)

#estimate MSE and PSNR
p3 = 'img_mse_ipol input_0.png output_1.png'
val3 = os.system(p3)

if val1 & val2 & val3 != 0:
	sys.exit("'noise.png' not found")

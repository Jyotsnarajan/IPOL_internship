#!/usr/bin/env python3

import argparse
import os


# parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("add_noise", type=str, default="True")
ap.add_argument("sigma", type=int)
ap.add_argument("speedup", type=str, default="False")
ap.add_argument("computebias", type=str, default="False")
ap.add_argument("dobestpsnr", type=str, default="False")
args = ap.parse_args()


def get_bool_param_from_string(string):
    """
    Returns 1 (True) or 0 (False) from the string value
    """
    test = str(string)            
    param = 1 if test == 'True' else 0
    return param

noise = get_bool_param_from_string(args.add_noise)
speedup = get_bool_param_from_string(args.speedup)
computebias = get_bool_param_from_string(args.computebias)
dobestpsnr = get_bool_param_from_string(args.dobestpsnr)


p = f'ksvd input_0.png {args.sigma} {noise} noisy.png denoised.png diff.png bias.png diff_bias.png {computebias} {speedup} {dobestpsnr}'
os.system(p)
if os.system(p)!= 0: exit(-1)

#!/usr/bin/env python3

import argparse
import os


# parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("add_noise", type=str, default="True")
ap.add_argument("sigma", type=int)
ap.add_argument("usearea1", type=str, default="True")
ap.add_argument("usearea2", type=str, default="False")
ap.add_argument("computebias", type=str, default="False")
args = ap.parse_args()


def get_bool_param_from_string(string):
    """
    Returns 1 (True) or 0 (False) from the string value
    """
    test = str(string)            
    param = 1 if test == 'True' else 0
    return param

add_noise = get_bool_param_from_string(args.add_noise)
usearea1 = get_bool_param_from_string(args.usearea1)
computebias = get_bool_param_from_string(args.computebias)
usearea2 = get_bool_param_from_string(args.usearea2)

p = f'NL_Bayes input_0.png {args.sigma} {add_noise} noisy.png denoised.png basic.png\
		diff.png bias.png basic_bias.png diff_bias.png {usearea1} {usearea2} {computebias}' 
os.system(p)

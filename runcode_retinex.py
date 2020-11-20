#!/usr/bin/env python3

import argparse
import shutil
import os
import os.path
import time
import PIL.Image

# parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("t", type=int)
args = ap.parse_args()

img = PIL.Image.open('./' + 'input_0.png')
general_params = '{}'.format(str(args.t))
params = 'input_0.png output_1.png'
exec_str = 'retinex_pde {} {}'.format(general_params, params)
os.system(exec_str)

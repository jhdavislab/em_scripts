'''Add scale bar to .mrc file'''
__author__ = "Joey Davis, www.jhdavislab.org"
__version__ = "1.0"


from cryodrgn import mrc
import matplotlib.pyplot as plt
from scipy import ndimage
import numpy as np

import argparse
import numpy as np
import sys, os

import matplotlib
import matplotlib.pyplot as plt

from cryodrgn import utils
from cryodrgn import mrc
from cryodrgn import analysis

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', help='MRC image file to process')
    parser.add_argument('pixel_size', help='Angstroms per pixel')
    parser.add_argument('--scale1', help='Optional scale bar 1 size in angstroms. Default 100A')
    parser.add_argument('--scale2', help='Optional scale bar 2 size in angstroms. Default 300A')
    parser.add_argument('--tiff', help='Output file as a .tiff. Default is the input_name.png')
    parser.add_argument('--gblur', help='Apply gaussian blur of a given amount. Example --gblur 5')

    return parser

def main(args):
    stack, _ = mrc.parse_mrc(args.input)
    image = stack[0]
    x_dim = image.shape[0]
    y_dim = image.shape[1]
    print('image dimensions: ' +str(stack.shape[1])+'x'+str(stack.shape[1])+' pixels')
    ang_px = float(args.pixel_size)
    if args.scale1:
        scale_a = float(args.scale1)
    else:
        scale_a = float(100)
    if args.scale2:
        scale_b = float(args.scale2)
    else:
        scale_b = float(400)
    line_a = scale_a/ang_px
    line_b = scale_b/ang_px
    offset = x_dim/20    

    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(10,10))
    if args.gblur:
        image = ndimage.gaussian_filter(image, float(args.gblur))
    axes.imshow(image, cmap='Greys_r')
    axes.plot(np.array([offset,offset+line_a]), np.array([y_dim-offset, y_dim-offset]), color='red')
    axes.plot(np.array([(offset*2+line_a)/2.0,(offset*2+line_a)/2.0]), np.array([y_dim-offset-y_dim/100, y_dim-offset+y_dim/100]), color='red')
    axes.text((2*offset+line_a)/2, y_dim-offset+y_dim/50, str(scale_a)+' A',color='r', ha='center', va='center')

    axes.plot(np.array([x_dim-offset,x_dim-offset-line_b]), np.array([y_dim-offset, y_dim-offset]), color='cyan')
    axes.plot(np.array([(2*x_dim-2*offset-line_b)/2.0,(2*x_dim-2*offset-line_b)/2.0]), np.array([y_dim-offset-y_dim/100, y_dim-offset+y_dim/100]), color='cyan')
    axes.text((2*x_dim-2*offset-line_b)/2.0, y_dim-offset+y_dim/50, str(scale_b)+' A',color='cyan', ha='center', va='center')

    axes.axis('off')
    if args.tiff:
        extension = '.tiff'
    else:
        extension = '.png'
    plt.savefig(args.input.split('.mrc')[0]+extension)
if __name__ == '__main__':    
    main(parse_args().parse_args())

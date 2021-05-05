'''View the top 9 images in a particle stack'''

import argparse
import numpy as np
import sys, os

import matplotlib
import matplotlib.pyplot as plt

from scipy import ndimage

from cryodrgn import utils
from cryodrgn import mrc
from cryodrgn import analysis

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', help='Particle stack')
    parser.add_argument('--lowpass', type=float, default=3, help='set lowpass filter level')
    parser.add_argument('-o', help='Output PNG')
    return parser

def main(args):
    stack, _ = mrc.parse_mrc(args.input,lazy=True)
    print('{} {}x{} images'.format(len(stack), *stack[0].get().shape))
    stack = [stack[x].get() for x in range(16)]
    plot_projections(stack, args.lowpass, args.o)

def plot_projections(stack, lowpass, output):
    fig, axes = plt.subplots(nrows=4, ncols=4, figsize=(10,10))
    axes = axes.ravel()
    for i in range(min(len(stack), 16)):
        axes[i].imshow(ndimage.gaussian_filter(stack[i], lowpass), cmap='Greys_r')
    for i in range(16):
        axes[i].axis('off')
    plt.tight_layout()
    if output:
        plt.savefig(output)
    else:
        plt.show()

if __name__ == '__main__':
    main(parse_args().parse_args())

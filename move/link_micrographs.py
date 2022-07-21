#!/home/jhdavis/anaconda3/bin/python
__author__ = "Joey Davis, www.jhdavislab.org"
__version__ = "1.1"

import os
import sys
import random
import argparse

def add_args(parser):
    parser.add_argument('root_dir', help='The root path for your collection data (should contain GridSquare folders and typically is Images-Disc1')
    parser.add_argument('output_path', type=str, help='path to the directory to write all of the symlinks. This directory must already exist.')
    parser.add_argument('extension', type=str, help='extension of the filename to link - typically _fractions.tiff or _fractions.mrc')
    parser.add_argument('--execute', default=False, action='store_true', help='peform the job instead of simply testing')
    return parser

def main(args):
    rootdir = args.root_dir
    extension = args.extension
    outdir = args.output_path

    if outdir[-1] != '/':
        outdir+='/'
    if rootdir[-1] != '/':
        rootdir+='/'

    num_total = 0
    for root, subdirs, files in os.walk(rootdir):
        if 'Data' in subdirs:
            print('Found Data directory in: '+root)
            data_files = os.listdir(root+'/Data/')
            data_images = [selected_file for selected_file in data_files if selected_file[-len(extension):]==extension]
            print('Found ' + str(len(data_images)) + ' data images.')
            for f in data_images:
                if args.execute:
                    os.symlink(root+'/Data/'+f, outdir+f)
                else:
                    print('*test** - with the --execute flag, would create smylink: ' + root+'/Data/'+f + '-->' + outdir+f)
            num_total+=len(data_images)

        elif 'GridSquare' in root.split('/')[-1]:
            print('No data directory found in: '+root+'. Check to see that you have transferred all data if you expected images/movies in this folder.')

    print('\nFound and linked '+ str(num_total) + ' data images.')

if __name__ =='__main__':
    argparser = argparse.ArgumentParser(
        description='Create symlinks to a subset of files within a nested collection directory. Typically used to pull a subset of movies for initial test processings.')
    add_args(argparser)
    main(argparser.parse_args())

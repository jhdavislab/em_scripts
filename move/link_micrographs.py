import os
import sys
import random
import argparse

def add_args(parser):
    parser.add_argument('root_dir', help='The root path for your collection data (should contain GridSquare folders and typically is Images-Disc1')
    parser.add_argument('output_path', type=str, help='path to the directory to write all of the symlinks. This directory must already exist.')
    parser.add_argument('extension', type=str, help='extension of the filename to link - typically _fractions.tiff or _fractions.mrc')
    parser.add_argument('fraction', type=float, help='fraction of the movies to link - typically 1.0 for all or 0.1 for 10%%.')
    parser.add_argument('--execute', default=False, action='store_true', help='peform the job instead of simply testing')
    return parser

def main(args):
    rootdir = args.root_dir
    extension = args.extension
    fraction = args.fraction
    outdir = args.output_path

    if outdir[-1] != '/':
        outdir+='/'

    num_total = 0
    num_selected = 0
    for root, subdirs, files in os.walk(rootdir):
        if 'GridSquare' in root.split('/')[-1]:
            print('Inspecting gridsquare: ' + root.split('/')[-1])
        if 'Data' in root.split('/')[-1]:
            data_images = [selected_file for selected_file in files if selected_file[-len(extension):]==extension]
            print('Found ' + str(len(data_images)) + ' data images.')
            num = int(len(data_images)*fraction)
            print('Selecting ' + str(num) + ' data images.')
            selected_images = random.sample(data_images, num)
            print('Creating symbolic links...')
            for f in selected_images:
                if vars(args)['execute']:
                    os.symlink(root+'/'+f, outdir+f)
                else:
                    print('*test* - would create smylink: ' + root+'/'+f + '-->' + outdir+f)
            num_total+=len(data_images)
            num_selected+=num

    print('\nFound '+ str(num_total) + ' data images. Linked ' + str(num_selected) + '.')

if __name__ =='__main__':
    argparser = argparse.ArgumentParser(
        description='Create symlinks to a subset of files within a nested collection directory. Typically used to pull a subset of movies for initial test processings.')
    add_args(argparser)
    main(argparser.parse_args())

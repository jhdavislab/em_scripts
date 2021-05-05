#!/home/jhdavis/anaconda3/envs/default/bin/python3
# -*- coding: utf-8 -*-

"""
@author: jhdavis@mit.edu : github.com/jhdavislab
"""

import argparse
import os
import glob

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Wrapper function for e2proc2d.py to convert a set of images. Requires that e2proc2d.py is in your path...run add_eman if necessary.',
                                    epilog='Example usage: python .py input_directory .png --options "--fouriershrink 2"')

    parser.add_argument('input_directory', type=str,
                       help='path to the directory to search for mrc files. Must be absolute path.')
    parser.add_argument('output_extension', type=str,
                       help='output exntesion (e.g. .png or .tiff')
    parser.add_argument('--options', default='',
                        help='additional options to pass to e2proc2d.py. must be in quotations"')
    parser.add_argument('--test', default=False, action='store_true',
                        help='used for testing - will only display the command to be executed, but will not actually run')

    args = parser.parse_args()

    input_dir= vars(args)['input_directory']
    if input_dir[-1] == '/':
        input_dir = input_dir[:-1]

    extension= vars(args)['output_extension']
    options = vars(args)['options'].split(' ')
    test = vars(args)['test']

    all_files = glob.glob(input_dir+'/*.mrc')
    for f in all_files:
        command = 'e2proc2d.py ' + f + ' ' + '.'.join(f.split('.')[:-1])+extension + ' ' + ' '.join(options)
        print('running: ' + command)
        if not(test):
            os.system(command)

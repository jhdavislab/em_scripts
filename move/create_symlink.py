#!/home/jhdavis/anaconda3/bin/python
__author__ = "Joey Davis, www.jhdavislab.org"
__version__ = "1.0"

import glob
import os
import numpy as np
import sys
import argparse

if __name__ =='__main__':
    parser = argparse.ArgumentParser(description='Create symlinks to .mrc files specified in a CryoSparc .cs file. This is most useful if you have curated micrographs in CryoSparc and now want to use those curated micrographs in Relion.')
    parser.add_argument('cs_file', type=str,
                       help='path to the cryosparc file - should be the output of curate micrographs. e.g. - ./passthrough_micrographs_accepted.cs')
    parser.add_argument('output_path', type=str,
                        help='path to the directory to write all of the symlinks. e.g. - /data/em/jhdavis/clpP/curated_symlink/')
    parser.add_argument('raw_path', type=str,
                        help='path to the directory containing all of the raw files. e.g. - /data/em/jhdavis/clpP/raw')
    parser.add_argument('--execute', default=False, action='store_true',
                        help='peform the job instead of simply testing')
    args = parser.parse_args()

    cs_file = vars(args)['cs_file']
    output_path = vars(args)['output_path']
    raw_path = vars(args)['raw_path']
    execute = vars(args)['execute']

if output_path[-1] != '/':
    output_path=output_path+'/'
if raw_path[-1] != '/':
    raw_path+=raw_path+'/'

cs_data = np.load(cs_file)

if execute:
    try:
        os.mkdir(output_path)
    except OSError:
        print ("***creation of the directory %s failed: check if the directory already exists and if you have permissions to write to that directory***" % output_path)
    else:
        print ("Successfully created the directory %s " % output_path)
else:
    print('=========TESTING ONLY, NOTHING WILL BE CHANGED===========')
    print("mkdir " + output_path)


good_micrographs = []
for micrograph in cs_data:
    name = micrograph[29].decode("utf-8").split('/')[-1]
    good_micrographs.append(name)

count = 0
for i in good_micrographs:
    source = raw_path+i
    dest = output_path+i

    if execute:
        try:
            os.symlink(source, dest)
        except OSError:
            print("***symlink to %s failed: check if the symlink already exists and if you have permissions to write to that directory***" %source)
        else:
            count+=1
            print("created symlink to %s" %source)
    else:
        print('ln -s ' + source + ' ' + dest)
if execute:
    print('successfully created: ' + str(count) + ' symbolic links in :' + output_path)
        

#!/home/jhdavis/anaconda3/bin/python
__author__ = "Joey Davis, www.jhdavislab.org"
__version__ = "1.1"

import argparse
import glob
import os
import sys
from shutil import copyfile

if __name__ =='__main__':
    parser = argparse.ArgumentParser(description='Pull all relevant image files into a single directory')
    parser.add_argument('top_directory', type=str,
                       help='path to the top directory')
    parser.add_argument('output_directory', type=str,
                        help='path to the directory to save all of the files')
    parser.add_argument('--file_type', default='.mrc', type=str,
                        help='string for the type of files to grab (e.g. .tiff, .mrc, etc')
    parser.add_argument('--filter', default='FoilHole_*_Data', type=str,
                       help='substring in your image files you want to search for')
    parser.add_argument('--test', default=False, action='store_true',
                        help='just list the files that would be copied, but do not actually do anything')
    parser.add_argument('--fractions', default=False, action='store_true',
                        help='remove any files with the string "Fractions"')
    parser.add_argument('--size', default=100, type=float,
                        help='minimum size of files you want included')
    args = parser.parse_args()

    top_dir = vars(args)['top_directory']
    output_dir = vars(args)['output_directory']
    file_type = vars(args)['file_type']
    filter_string = vars(args)['filter']
    test_only = vars(args)['test']
    remove_fractions = vars(args)['fractions']
    size_limit = vars(args)['size']

    if test_only==True:
        print('=========TESTING ONLY, NOTHING WILL BE CHANGED===========')
    else:
        try:
            os.mkdir(output_dir)
            print("Directory " , output_dir ,  " created...") 
        except FileExistsError:
            print("Directory " , output_dir ,  " already exists")
            proceed = input("\nProceed? [y/n]").upper()
            if proceed=='N':
                sys.exit()

    search_string = top_dir+'/**/*'+filter_string+'*'+file_type
    
    print("finding files matching the following: "+search_string+'...')
    all_image_files_pre = glob.glob(search_string, recursive=True)
    all_image_files = [i for i in all_image_files_pre if os.stat(i).st_size >= size_limit]
    all_image_files.sort()
    
    if remove_fractions:
        for image in all_image_files:
            if "Fractions" in image:
                all_image_files.remove(image)

    print('found '+str(len(all_image_files))+' files...\n')
    
    print('first and last 3 files are: ')
    for image_name in all_image_files[:3] + all_image_files[-3:]:
        print(image_name)
    print('\nthe last file output will be:')
    new_name = output_dir+'/'+image_name.split('/')[1]+'_'+image_name.split('/')[-1]
    print(new_name)
    proceed = input("\nProceed? [y/n]").upper()
    
    if proceed=='Y':
        print('OK, as you wish...')
        for image_name in all_image_files:       
            new_name = output_dir+'/'+image_name.split('/')[1]+'_'+image_name.split('/')[-1]
            if test_only==False:
                copyfile(image_name, new_name)
            else:
                print('cp '+image_name+' '+new_name)
    print('file copy complete!')
    sys.exit()

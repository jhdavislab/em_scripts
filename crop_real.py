#!/home/jhdavis/anaconda3/envs/default/bin/python3
# -*- coding: utf-8 -*-

"""
@author: jhdavis@mit.edu : github.com/jhdavislab
"""

import argparse
import os
import edit_cs

def crop_stack(input_stack, output_stack, dim_x, dim_y, e2_path=''):
    if e2_path is '':
        e2_path = 'e2proc2d.py'
    execution_string = e2_path + ' --clip ' + str(dim_x) + ',' + str(dim_y) + ' ' + input_stack + ' ' + output_stack
    print("preparing to execute the following:")
    print(execution_string)
    if test is False:
        print('executing...')
        os.system(execution_string)
    else:
        print('running in test mode, so no command was executed.')

if __name__ =='__main__':
    parser = argparse.ArgumentParser(description='Crop a particle stack in real space. Optionally edits a cryosparc .cs file to reflect the new box size. Requires e2proc2d.py is in your path! Note that this tool simply crops about the center of the image.',
                                    epilog='Example usage: python3 crop_real.py input_stack.mrcs output_stack.mrcs 128,96 --cs_file cryosparc_v2_csfile.cs')

    parser.add_argument('input_stack', type=str,
                       help='path to the input .mrcs stack')
    parser.add_argument('output_stack', type=str,
                       help='path to the output .mrcs stack')
    parser.add_argument('crop_dimensions', type=str,
                        help='dimensions to crop. Provided as x_dim,y_dim (e.g. 128,96)')
    parser.add_argument('--cs_file', default='',
                        help='path to the cryosparcv2.cs file (expected export output from a 2D classification job)')
    parser.add_argument('--test', default=False, action='store_true',
                        help='used for testing - will only display the command to be executed, but will not actually run')
    parser.add_argument('--e2path', default='',
                        help='provide a full path to the e2proc2d.py file. If not provided, this file MUST be in your PATH')
    args = parser.parse_args()

    input_stack= vars(args)['input_stack']
    output_stack= vars(args)['output_stack']
    cs_file = vars(args)['cs_file']
    e2_path = vars(args)['e2path']
    test = vars(args)['test']
    dims = vars(args)['crop_dimensions']
    dim_x, dim_y = dims.split(',')

    crop_stack(input_stack, output_stack, dim_x, dim_y, e2_path)
    if cs_file!='':
        print("...editing .cs file to reflect the new box size. New file will be:")
        new_file_name = cs_file.split('.cs')[0]+'_'+dim_x+'x'+dim_y+'.cs'
        print(new_file_name)

        np_cs = edit_cs.parse_cs(cs_file)
        np_cs_new = edit_field(np_cs, 'blob/shape', ':', dim_x+','+dim_y)
        edit_cs.write_cs(new_file_name, np_cs_new)

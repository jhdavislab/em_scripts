#!/home/jhdavis/anaconda3/envs/default/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 20:49:28 2019

@author: jhdavis@mit.edu : github.com/jhdavislab
"""

import argparse
import numpy as np

def parse_cs(file_name):
    '''parse_cs parases a cryosparcv2 file and return a numpy object with each field and each particle. 
        For example, the df1_A field for particle 20 (0 indexed) is found in np_cs['ctf/df1_A'][20]

    Args:
        file_name (string to the cs file): string pointing to a cs file (must provide full path)

    Returns:
        a numpy object resulting from loading the .cs file

    Usage:
        np_cs= parse_cs('./test.cs)
    '''

    return np.load(file_name)

def get_fields(np_cs):
    '''get_fields reads a numpy cryosparcv2 object (output of parse_cs) and returns dictionary with a list 
        of the fields and the total number of particles. 

    Args:
        np_cs (a numpy object): should be the output of parse_cs

    Returns:
        a dictionary with keys 'fields' and num_particles'

    Usage:
        info = get_fields(np_cs)
    '''
    
    return {'fields': list(np_cs.dtype.fields.keys()), 'num_particles': np_cs.shape[0]}

def edit_field(np_cs, field, index, new_value):
    '''edit_field edits a cryosparc numpy object replacing the values of all particles provided in the index (this
    uses typical numpy indexing) and in the given field (a string) with the new value. Returns the updated cryosparc
    numpy array.

    Args:
        np_cs (a numpy object): should be the output of parse_cs
        field (string): a string specifying which field to edit. Must be contained in the set of fields
        index (numpy indexing): any object that can be used to index a numpy array. This should be a tuple with the desired index.
        new_value (string): a string wiht the new value to insert

    Returns:
        new_np_cs (a numpy object): the updated numpy cryosparc object

    Usage:
        edited_spherical_ab = edit_field(np_cs, 'ctf/cs_mm', ':', 2.7)
    '''
    
    info = get_fields(np_cs)
    all_fields = info['fields']
    assert field in all_fields
    
    np_cs[field][index] = new_value
    return np_cs

def write_cs(output_file_name, np_cs):
    '''Write a cs file given numpy cs file

    Args:
        output_file_name (string): path and filename to write
        np_cs (numpy object): 

    Usage:
        write_cs('./modified_cs.cs, np_cs)
    '''

    with open(output_file_name, 'wb') as outfile:
        np.save(outfile, np_cs)
    
if __name__ =='__main__':
    parser = argparse.ArgumentParser(description='Edit a cryosparcv2 file',
                                    epilog='Example usage: python3 edit_cs.py input.cs output.cs ctf/cs_mm 2.7 --particle_index 0:100')
    parser.add_argument('input_file', type=str,
                       help='path to the file to edit')
    parser.add_argument('output_file', type=str,
                       help='path to the file to write')
    parser.add_argument('field_to_edit', type=str,
                        help='field to edit')
    parser.add_argument('new_value', type=str,
                        help='string to insert in this field')
    parser.add_argument('--particle_index', default=':',
                        help='optional string to index by particle numbers')
    args = parser.parse_args()

    input_file= vars(args)['input_file']
    output_file= vars(args)['output_file']
    field= vars(args)['field_to_edit']
    new_value = vars(args)['new_value']
    particle_index = vars(args)['particle_index']

    np_cs = parse_cs(input_file)
    np_cs_new = edit_field(np_cs, field, particle_index, new_value)
    write_cs(output_file, np_cs_new)

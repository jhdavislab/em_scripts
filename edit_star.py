#!/home/jhdavis/anaconda3/envs/default/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 20:49:28 2019

@author: jhdavis@mit.edu : github.com/jhdavislab
"""

import pandas as pd
import argparse
import re

def parse_star(file_name):
    '''parase a star file and return a dictionary with keys 'preamble', 'header', 'data', 'start_row', 'space_sequence'.
    * preamble consists of all lines preceeding the 'loop_' keyword.
    * header consists of each of the lines following 'loop_' and preceeding the data.
    * data is a pandas dataframe with the data entries (column headers are taken from the header)
    * start_row indicates the row on which data actually starts
    * space_sequence indicates the column separator spacing found in the first data row (list of integers)

    Args:
        file_name (string to the star file): string pointing to a star file
    
    Returns:
        a dictionary as follows:
        keys 'preamble', 'header', 'data', 'start_row', 'space_sequence'.
        * preamble list consists of all lines preceeding the 'loop_' keyword.
        * header list consists of each of the lines following 'loop_' and preceeding the data.
        * data list consists of each of the lines of data.
        * dataframe is a pandas dataframe with the data entries (column headers are taken from the header)
        * start_row indicates the row on which data actually starts
        * space_sequence indicates the column separator spacing found in the first data row (list of spaces)

    Usage:
        my_star= parse_star('./test.star)
    '''
    
    with open(file_name) as f:
        preamble = []
        skipped_lines = 0
        line = f.readline()
        skipped_lines+=1
        while(not 'loop_' in line):
            preamble.append(line)
            line = f.readline()
            skipped_lines+=1
        preamble.append(line)
        header = []
        line = f.readline()
        skipped_lines+=1
        while line[0] == '_':
            header.append(line.split(' ')[0])
            position = line.split('#')[-1]
            assert int(len(header))==int(position),'Error with the .star file header - number of elements not matched to the reported "#" in '+header[-1]
            line = f.readline()
            skipped_lines+=1
        data = []
        data.append(line)
        data = data+f.readlines()
        spaces = re.findall('\s+', data[0])
        df = pd.read_csv(file_name, skiprows = skipped_lines-1, sep='\s+', names=header)
        
    return {'preamble':preamble, 'header':header, 'data':data, 'dataframe':df, 'start_row':skipped_lines-1, 'space_sequence':spaces}

def edit_star(dataframe, column, search_string, replace_string, regex=False):
    '''Edit the data in a parsed star file (stored as a pandas dataframe - the output of parse_star).
    This function simply uses Series.str.replace (see https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.replace.html)

    Args:
        dataframe (pandas dataframe): should be the parsed data from a .star file
        column (string): the column to edit
        search_string (string): a string to replace in the given column
        replace_string (string): string to insert
        regex (bool, optional: default=False): choice to use regex parsing
    
    Usage:
        mod_dataframe = edit_star_data(star_data, '_rlnImageName', 'Extract', 'Joey')
    '''
    dataframe[column] = dataframe[column].str.replace(search_string, replace_string, regex=regex)
    return dataframe

def write_star(output_file_name, star_dictionary):
    '''Write a star file given a parsed star_dictionary
    
    Args:
        output_file_name (string): path and filename to write
        star_dictionary (hash): should have the same structure as the output of parse_star (keys='preamble', 'header', 'data', 'start_row, 'space_sequence)
    
    Usage:
        write_star('./modified_star.star, star_dictionary)
    '''

    df = star_dictionary['dataframe']    
    cols = df.columns
    spaces = star_dictionary['space_sequence']    
    with open(output_file_name, 'wb') as outfile:
        outfile.writelines(star_dictionary['preamble'])
        for col_index, col_name in enumerate(star_dictionary['header']):
            outfile.write(col_name + ' ' + '#' + str(col_index+1) + '\n')
        for row in range(df.shape[0]):
            line = ''
            for index in range(len(cols)):
                line = line + spaces[index] + str(df.iloc[row,index])
            outfile.write(line+spaces[-1])

if __name__ =='__main__':
    parser = argparse.ArgumentParser(description='Edit a star file',
                                    epilog='Example usage: python3 edit_star.py input.star output.star _rlnImageName Extract --replacement_string Joey')
    parser.add_argument('input_file', type=str,
                       help='path to the file to edit')
    parser.add_argument('output_file', type=str,
                       help='path to the file to write')
    parser.add_argument('column_to_edit', type=str,
                        help='column to edit')
    parser.add_argument('string_to_replace', type=str,
                        help='string to replace (original)')
    parser.add_argument('--replacement_string', default='',
                        help='string to insert (new). Defaults to simply removing the old string.')
    parser.add_argument('--regex', default=False, action='store_true',
                        help='use the regular expression module in doing the search')
    args = parser.parse_args()

    input_file= vars(args)['input_file']
    output_file= vars(args)['output_file']
    column= vars(args)['column_to_edit']
    source_string = vars(args)['string_to_replace']
    new_string = vars(args)['replacement_string']
    use_regex = vars(args)['regex']
    
    my_star = parse_star(input_file)
    my_star['dataframe'] = edit_star(my_star['dataframe'], column, source_string, new_string, regex=use_regex)
    write_star(output_file, my_star)

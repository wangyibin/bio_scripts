#!/usr/bin/env python
# -*- coding=utf-8 -*-

## Author:Wangyibin
## Time:Aug 22 2018

## Description:To caculate a column value mean 

usage = """pyhton get_mean.py infile column_num"""

from numpy import array
from numpy import mean
from sys import argv


def read_file(infile,column_num):

        """read file and store in list"""

        
        column_list = []

        with open(infile,'r') as f:

                fl = f.readlines()

                for line in fl:
                        
                        
                        value = int(line.split()[int(column_num)-1])
                        column_list.append(value)


        return column_list
                

def out_mean_value(infile,column_num):

        """caculate the mean depth and out in a file"""

    
        column_list = read_file(infile,column_num)
        
        np_array = array(column_list)
        mean_value = mean(np_array)

        return mean_value


                
                    
if __name__ == "__main__":

        if len(argv) == 3:
                infile = argv[1]
                column_num = argv[2]
        
                mean_value = out_mean_value(infile,column_num)
        
                out = '%s\t%s\n'%(infile.split('.')[0],mean_value)
                print(out)

        else :

                print('ERROR: %s'%usage)



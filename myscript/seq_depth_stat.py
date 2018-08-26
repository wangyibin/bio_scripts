#!/usr/bin/env python
# -*- coding=utf-8 -*-

## Author:Wangyibin


from numpy import array
from numpy import mean
from sys import argv


def read_depth(depthfile):

        """read depth file and store in list"""

        
        depth_dict = {}

        with open(depthfile,'r') as f:

                fl = f.readlines()

                for line in fl:
                        chrom = line.split()[0]
                        
                        depth = int(line.split()[2])
                                                                       
        
                        if chrom in depth_dict.keys():

                                depth_dict[chrom].append(depth)
                        else:
                                depth_dict[chrom] = [depth]


        return depth_dict
                

def out_mean_depth(depthfile):

        """caculate the mean depth and out in a file"""

        depth_dict = read_depth(depthfile)

        with open('mean_depth.txt','w') as o:
                s = 0
                for chrom in depth_dict.keys():
                        np_array = array(depth_dict[chrom])
                        mean_depth = mean(np_array)
                        
                        s = s + mean_depth
                        o.write('%s\t%s\n'%(chrom,mean_depth))

                total_mean_depth = s/(len(depth_dict.keys()))
                o.write('%s\t%s\n'%('total_mean_depth',total_mean_depth))


                
                    
if __name__ == "__main__":


        depthfile = argv[1]

        out_mean_depth(depthfile)

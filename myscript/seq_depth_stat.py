#!/usr/bin/env python
# -*- coding=utf-8 -*-

## Author:Wangyibin
"""
%prog -b bamfile -o outprefix [options]

Caculate the sequence mean depth from a bam file.
For example, to get the bam sequences mean depth, do this::
    %prog -b sorted.bam -o out -w True

"""

from numpy import array
from numpy import mean
from os import system
import sys


def create_depth_file(bamfile):
    """
    use the samtools depth to caculate the sequence depth
    """
    system("samtools depth %s > depth.txt"%(bamfile))
    depthfile = 'depth.txt'
    
    return depthfile


def read_depth(depthfile):

    """read depth file and store in list"""
        
    depth_list = []
        
    with open(depthfile,'r') as f:

        fl = f.readlines()

        for line in fl:
            #chrom = line.split()[0]
                        
            depth = float(line.split()[2])

            depth_list.append(depth)


    return depth_list
                

def out_mean_depth(bamfile,out_prefix,out_whether=False):

    """
    caculate the mean depth and out in a file or print
    """

    depthfile = create_depth_file(bamfile)
    depth_list = read_depth(depthfile)
    
    np_array = array(depth_list)
    mean_depth = mean(np_array)

    if out_whether:
        print('%s\t%s'%(out_prefix,mean_depth))

    else:
        with open('mean_depth.txt','w') as o:
            o.write('%s\t%s\n'%(out_prefix,mean_depth))


        
                    
if __name__ == "__main__":

    from optparse import OptionParser
        
    p = OptionParser(__doc__)
    p.add_option('-b','--bamfile',dest='bamfile',
                    help='input bamfile')

    p.add_option('-o','--outprefix',dest='outprefix',
                    help='the out file or print prefix')
    p.add_option('-w','--write_whe',dest='write_whe',
                    help='out the result to a file whether or not [default=False] ')
    
    opts,args = p.parse_args()
    print(len(sys.argv))
    if len(sys.argv) < 6:
        sys.exit(p.print_help())

    

    out_mean_depth(opts.bamfile,opts.outprefix,opts.write_whe)

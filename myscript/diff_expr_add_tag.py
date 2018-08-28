#!/usr/bin/env python
# -*- coding=utf-8 -*-

## Author:WangYibin
## Time:Aug 25 2018

"""
##############################################################
        
Usage:python %prog infile outfile

Add tag to the bed file from difference expression analysis
        
                                        Copyright:Yibin Wang

##############################################################
"""


from sys import argv
from subprocess import call


def diff_expr_add_tag(infile,outfile):
    """
    add tag to the bed file from difference expression analysis,
    and output in a new bed file
    """

    print("Running...")
    #extract id fc q_val
    call("cut -f1,3,5 %s > diff.bed"%infile,shell=True)
    
    o = open(outfile,'w')

    with open('diff.bed','r') as f:
        head = f.readline()
        head = head.strip() + 'tag\n'
        o.write(head)

        
        for line in f.readlines():
            line_list = line.split()
            tag ='NA'
            fc = line_list[1]
            q_val = line_list[2]
            
            if (fc != 'NA') and (q_val != 'NA'):
                fc = float(fc)
                q_val = float(q_val)

                if (fc > 1) and (q_val < 0.05):
                    tag =  'up'
                elif (fc < 1) and (q_val < 0.05):
                    tag = 'down'
                elif (q_val > 0.05):
                    tag = 'notsig'
                
            line_list.append(tag)
            s = ''
            for item in line_list:
                s = s + item.strip() + '\t'

            o.write(s + '\n')
    
    o.close()

    call("rm diff.bed",shell=True)
    print('Done')



if __name__ == "__main__":
    
    if len(argv) == 3:
        print(__doc__)
        infile,outfile = argv[1],argv[2]

        diff_expr_add_tag(infile,outfile) 
    else:
        print('ERROR:')
        print(__doc__)


                


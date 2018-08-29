#!/usr/bin/env python
# -*- coding=utf-8 -*-

## Author:WangYibin
"""
%prog [options]

To out the nucmer command and qsub.
"""

from subprocess import call
import sys

def out_nucmer_cmd(ref,sp_dir,sp_list,suffix):
    """

    """
    with open(sp_list,'r') as f:
        
        head = """#!/bin/bash\n#$ -cwd\n#$ -S /bin/bash\n#$ -j y\n#$ -pe mpi 1\n#$ -q all.q\n"""
        for line in f.readlines():
            sp_name = line.strip('\n')

            with open('run.%s.sh'%sp_name,'w') as o :

                o.write(head)
                cmd = "\n\
/public1/home/zhangxt/bin/nucmer %s %s "%(ref,sp_dir)+str(sp_name)+str(suffix)+" --prefix "+str(sp_name)+"out\n\
Assemblytics "+str(sp_name)+"out.delta "+str(sp_name)+"_sv 1000 /public1/home/zhangxt/software/Assemblytics-master\n\
delta-filter -r -q "+str(sp_name)+"out.delta > "+str(sp_name)+"out.filter.delta\n\
show-snps -Clr "+str(sp_name)+"out.filter.delta > "+str(sp_name)+"out.snps\n"
                        
                o.write(cmd)
            call('qsub run.%s.sh'%sp_name,shell=True)


                        

if __name__ == "__main__":

    from optparse import OptionParser
    p = OptionParser(__doc__)

    p.add_option('-r','--reference',dest='reference',
                  help="the reference file")
    p.add_option('-d','--sample_dir',dest='sample_dir',
                  help='the path of sample')
    p.add_option('-l','--sample_list',dest='sample_list',
                  help='the name list of sample')
    p.add_option('-s','--suffix',dest='suffix',
                  help='the suffix of sample')

    opts,args = p.parse_args()

    if len(sys.argv) < 9:
        sys.exit(p.print_help())
    
    out_nucmer_cmd(opts.reference,opts.sample_dir,opts.sample_list,opts.suffix)

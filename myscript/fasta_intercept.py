#!/usr/bin/env python
# -*- coding=utf-8 -*-

## Author:WangYibin

"""
%prog -f fasta -c chromosome -s start -e end

To intercept the sequence fragment by a position information.
                                            
                                        Copyright:WangYibin
"""

import sys
from Bio.SeqIO import parse
from optparse import OptionParser


def fasta_intercept(fastafile,chrn,start,end):

    """
    
    """
    
    fa_dict = {}

    with open(fastafile,'r') as f:
        fa = parse(f,'fasta')
        
        for record in fa:
            fa_dict[record.id] = str(record.seq)

    seq = fa_dict[chrn][start-1:end]
    return seq


if __name__ in "__main__":

    p = OptionParser(__doc__)

    p.add_option("-f","--fasta",dest="fasta",
                  help="input fasta file")
    p.add_option("-c","--chrn",dest="chromosome_name",
                  help="search chromosome name")
    p.add_option("-s","--start",dest="start",type='int',
                  help="the start position of search sequence")
    p.add_option("-e","--end",dest="end",type='int',
                  help="the end position of search sequence")

    opts,args = p.parse_args()
    
    if len(sys.argv[1:]) != 8:
        sys.exit(p.print_help())
        
    seq = fasta_intercept(opts.fasta,opts.chromosome_name,opts.start,opts.end)
    print(seq)

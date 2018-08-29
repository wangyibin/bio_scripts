#!/usr/bin/env python
# -*- coding=utf-8 -*-

## Author:WangYibin
"""
Usage:
python %prog fasta > chromlength.txt
"""

from Bio.SeqIO import parse
from sys import argv


def get_chr_length(infasta):
    """

    """
    with open(infasta,'r') as f:
        fa = parse(f,'fasta')

        for record in fa:
            print('%s\t%d'%(record.id,len(str(record.seq))))


if __name__ == "__main__":
    
    if len(argv) != 2:
        print('ERROR:')
        print(__doc__)
    else:
        infasta = argv[1]

        get_chr_length(infasta)

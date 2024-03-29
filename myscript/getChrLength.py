#!/usr/bin/env python
# -*- coding=utf-8 -*-

## Author:WangYibin
"""
Usage:
python %prog fasta [chromosome_name] > chromlength.txt

Return the length of each sequence in the fasta file.
                                    Copyright:WangYibin

"""

from Bio.SeqIO import parse
from sys import argv


def get_chr_length(infasta,chrn="all"):
    """

    """
    with open(infasta,'r') as f:
        fa = parse(f,'fasta')

        for record in fa:
            if chrn == "all":
                print('%s\t%d'%(record.id,len(str(record.seq))))
            elif chrn == record.id:
                print('%s\t%d'%(record.id,len(str(record.seq))))
                break
            else:
                print('chromosome name error, please'
                        ' input incorrect chromosome name of your fasta')


if __name__ == "__main__":
    
    if len(argv) < 2 or len(argv) > 3:
        print('ERROR:')
        print(__doc__)
        sys.exit()
    elif len(argv) == 3: 
        chrn = argv[2]

    infasta = argv[1]
    get_chr_length(infasta,chrn)

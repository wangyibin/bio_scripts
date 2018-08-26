#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author:WangYibin
# Time:Jul 12 2018

# Purpose:To remove the geneid.suffix in fasta ,in order to easy_KaKs.pl

# Usage: python $0 infile outfile

import sys
from Bio import SeqIO

def rm_point(infile,outfile):

	f = SeqIO.parse(infile,'fasta')
	with open(outfile,'w') as output_handle:
		for record in f:
			new_id = record.id.split('.')[0]
			record.id = new_id
			record.name = new_id
		#	seq = record.seq
		
		#	read = '>%s\n%s\n'%(new_id,seq)
			SeqIO.write(record,output_handle,'fasta')
		#	output_handle.write(read)
			
		


if __name__ == '__main__':
#	infile = sys.argv[1]
#	outfile = sys.argv[2]
#	rm_point(infile,outfile)
#	try:
#		sys.argv[2]
#	except:
#                print('usage')
	infile = sys.argv[1]
	outfile = sys.argv[2]
	rm_point(infile,outfil)


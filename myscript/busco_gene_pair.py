#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author:WangYibin
# Time: Jul 12 2018

# Purpose:to pair the gene from busco out

## Usage: python $0 file1 file2 


import sys

def create_dict1(file):
	with open(file,'r') as f:
		
		gene_dict = {}
		for line in f.readlines()[5:]:
			gene_list = line.split()
			gene_dict[gene_list[0]] = gene_list[2]	
		return gene_dict

def create_dict2(file):
        with open(file,'r') as f:
 
                 gene_dict = {}
                 for line in f.readlines()[5:]:
                         gene_list = line.split()
                         gene_dict[gene_list[0]] = gene_list[2].split('.')[0]                  
                 return gene_dict
	
def pair_gene(file1,file2):
	file1_dict = create_dict1(file1)
	file2_dict = create_dict1(file2)
	outfile = open('group.txt','w')
#	outfile = open(file1.split('_')[2].split('.')[0]+"-"+
#				file2.split('_')[2].split('.')[0]+'.tsv','w')

	for i in file1_dict.keys():
		if i in file2_dict.keys():
			o = '%s\t%s\n'%(file1_dict[i],file2_dict[i])
				
			outfile.write(o)
	
	outfile.close()

if __name__ == '__main__':
	file1 = sys.argv[1]
	file2 = sys.argv[2]	
	
	pair_gene(file1,file2)	

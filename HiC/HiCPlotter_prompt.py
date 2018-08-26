#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author:WangYibin
# Time:Jun 29 2018

# To print HiCPlotter prompt

import sys
from subprocess import call

def print_prompt(file_dir,sample_name,cluster_n):
	f = open('run_hicplotter.sh','w')
	sh_f = '#!/bin/bash\n#$ -cwd\n#$ -S /bin/bash\n#$ -j y\n#$ -pe mpi 1\n#$ -q all.q\n'
	f.write(sh_f)

	
	chr_sizes = {'20k':20000,'40k':40000,'150k':150000,'500k':500000,'1M':1000000}
	chr_lists = [ 'g%s'%(chr) for chr in range(1,int(cluster_n)+1)]
	
	for chr in chr_lists:
		 for chr_sizes_key in chr_sizes.keys():
			chr_size = chr_sizes[chr_sizes_key]	
			prompt1 = 'python ~/software/HiCPlotter/HiCPlotter.py -ext pdf -f %s/matrix/%s/iced/%s/%s_%s_iced.matrix -o %sout -r %s -tri 1 '%(file_dir,sample_name,chr_size,sample_name,chr_size,chr_sizes_key,chr_size) + '-bed %s/matrix/%s/raw/%s/%s_%s_ord.bed -n %s_%sRes -chr %s\n'%(file_dir,sample_name,chr_size,sample_name,chr_size,chr,chr_sizes_key,chr)
			f.write(prompt1)

	for chr_sizes_key in chr_sizes.keys():
		chr_size = chr_sizes[chr_sizes_key]
		chr = chr_lists[-1]
		prompt2 = 'python ~/software/HiCPlotter/HiCPlotter.py -ext pdf -f %s/matrix/%s/iced/%s/%s_%s_iced.matrix -o %sout -r %s -tri 1 '%(file_dir,sample_name,chr_size,sample_name,chr_size,chr_sizes_key,chr_size) + '-bed %s/matrix/%s/raw/%s/%s_%s_ord.bed -n Whole_genome_Res -wg 1 -chr %s\n'%(file_dir,sample_name,chr_size,sample_name,chr_size,chr)		
				
		f.write(prompt2)

        f.close()
	cmd = 'qsub run_hicplotter.sh'	
	call(cmd,shell=True)
if __name__ == '__main__':
	file_dir    = sys.argv[1]
	sample_name = sys.argv[2]
	cluster_N         = sys.argv[3]
	
	print_prompt(file_dir,sample_name,cluster_N)
	

#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author:WangYibin
# Time:Jun 25 2018

# To optimize clm from allhic

# usage python allhic_optimize.py cluster_N
import sys
from subprocess import call

prompt_front = '''
#!/bin/bash
#$ -cwd
#$ -S /bin/bash
#$ -j y
#$ -pe mpi 10
#$ -q all.q
'''

def write(i):
	i = int(i)
	for j in range(0,i):
		with open('run_optimize_g%s.sh'%(j),'w') as f:
			f.write(prompt_front)
			prompt = '/public1/home/zhangxt/bin/allhic optimize group%s.clm'%(j)
			f.write(prompt)
			f.close()
		cmd = 'qsub run_optimize_g%s.sh'%(j)
		call(cmd,shell = True)
if __name__ == '__main__':
	i = sys.argv[1]
	write(i)

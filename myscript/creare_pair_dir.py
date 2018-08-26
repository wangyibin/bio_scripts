#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author:WangYibin
# Time:Jul 20 2018

# Purpose:To create dir from busco to pair two species and copy the busco_result to this dir


import os,sys,shutil

sample = os.listdir('../busco/')
sample_copy = sample

while len(sample_copy) != 0:

	first = sample_copy.pop(0)
	for last in sample_copy:
	
		dir = '%s-%s'%(first.split('_')[1],last.split('_')[1])
	#	print(dir)	
		os.mkdir(dir)
		shutil.copy('../busco/%s/full_table_%s.new.tsv'%(first,first.split('_')[1]),'./%s'%(dir))
		shutil.copy('../busco/%s/full_table_%s.new.tsv'%(last,last.split('_')[1]),'./%s'%(dir))

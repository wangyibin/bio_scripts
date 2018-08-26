#!/usr/bin/env python
# -*- coding:utf-8 -*-


# Author:WangYibin
# Time:Jul 12 2018
# Purpose:To caculate the divergence time among two species

# Usage:python $0 ks.txt


import sys

def get_data(infile):

	with open(infile,'r') as f:
		data = []
		for line in f.readlines():
			l = line.strip()
		
			if l:		
				data.append(float(l))
	return data

def get_pair_num(infile):
	with open(infile,'r') as f:
		pair_num = len(f.readlines())/2
	
	return pair_num

def get_median(infile):
	data = get_data(infile)
	data.sort()
	half = len(data) // 2
	
	return ((data[half] + data[~half]) / 2)

def get_divergence_time(ks_median):
	dt = ks_median/(2*6.5*10**(-9))/1000000	

	return dt

def print_result(infile):
	pair_num = get_pair_num(infile)
	ks_median = get_median(infile)
	dt = get_divergence_time(ks_median)

	print('%s\t%s\t%s\t%s'%(infile.split('.')[0],pair_num,ks_median,str(round(dt,2))))


if __name__ == '__main__':

	infile = sys.argv[1]
	print_result(infile)

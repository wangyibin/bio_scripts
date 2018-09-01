#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys,os
from numpy import array
from matplotlib import pyplot

def get_data(inputfile):

	'''Usage:python draw_dp.py [inputfile]'''

	lenths = []
	readfile = open(inputfile)
	lines = readfile.readlines()
	
	for line in lines:	
		line = int(line)
		lenths.append(line)
	lenths = array(lenths)	
	
	xticks = array(list(range(0,600,25)))
	pyplot.hist(lenths,10000)
	pyplot.xlim(0,600)
	pyplot.xticks(xticks)
	
	pyplot.xlabel('DP')
	pyplot.ylabel('Frequency')	
	pyplot.title('Frequency of DP')

	pyplot.savefig(inputfile + '.hist.png')


if __name__ == '__main__':
	inputfile = sys.argv[1]
	get_data(inputfile)

	

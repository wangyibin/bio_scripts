#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Usage: %prog vcffile xlim

For vcf clean to draw the frequency distribution histogram of DP.
    
                                                Copyright:WangYibin

"""

import sys,os
from numpy import array
from matplotlib import pyplot
from pysam import VariantFile

def get_DP(vcffile):
    """
    Use the pysam VariantFile to read the vcffile 
    and store the DP into a list
    """
    print("Start read vcf file...")
    try:
        VariantFile
    except NameError:
        from pysam import VariantFile

    vcf_in = VariantFile(vcffile)
    DP_list = []

    for rec in vcf_in.fetch():
        DP_list.append(rec.info["DP"])

    return DP_list


def plot_dp_fre_dis(DP_list,xlim):
    """
    Plot the frequencY distribution histogram of DP
    """
    try:
        array
    except NameError:
        from numpy import array
    
    try:
        pyplot
    except NameError:
        from matplotlib import pyplot
    print(len(DP_list))
    DP_array = array(DP_list)
    xr = [50000,10000,5000,1000]
    for i in xr:
        if xlim//i > 10:
            xscale = i
            xticksn = ["%dk"%x for x in (range(0,xlim//xscale))]
            break
        elif xlim//1000 < 10:
            xscale = 500
            xticksn = [x for x in (range(0,xscale))]
        else:
            continue
    #label
    pyplot.xlabel('DP')
    pyplot.ylabel('Frequency')
    pyplot.title('Frequency of DP')
    
    #plot
    xticks = array(list(range(0,xlim,xscale)))
    pyplot.hist(DP_array)
    pyplot.xticks(xticks,xticksn)
    pyplot.xlim(0,xlim)
    #plot output
    pyplot.savefig(vcffile.strip(".vcf") + '.dp.hist.png')
    
    print("DP frequency distribution histogram have drawed "
            "and store in %s.dp.his.png"%vcffile.strip(".vcf"))


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

    if len(sys.argv) != 3:
        print("ERROR:")
        print(__doc__)
        sys.exit()

    vcffile = sys.argv[1]
    xlim = int(sys.argv[2])
    DP_list = get_DP(vcffile)

    plot_dp_fre_dis(DP_list,xlim)

	

#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
        %prog [options]

To covert the vcf file to a matrix file of the chl or all gene
    are single copy gene.
                                            
                                            Copyright:WangYibin
                                                Time:Aug 3 2018
"""

import sys 
from os import system
from Bio.SeqIO import parse


def get_sample_dict(vcffile):
	
	"""Get a sample_dict, which is {'tag0':sample_name0,'tag1':sample_name1,....}"""
	"""Usage:get_sample_dict(vcffile)"""
        
	with open(vcffile,'r') as f:
                
                active = True
                while active:
                        line = f.readline()
                        if line.startswith("##"):
                                continue
                        elif line.startswith("#"):
		                head = line.lstrip("#").split()[9:]
		                sample_num = len(head)
		                sample_dict = {}
                                active = False

		for i in range(0,sample_num):
			locals()['tag' + str(i)] = head[i].strip(">").strip("<")
			sample_dict['tag%s'%i] = locals()['tag' + str(i)]

	return sample_dict


def create_vcf_dict(vcffile):
	
	"""Create a vcf dict {ctg:{pos:{'REF':REF,'ALT':ALT,'tag0':sample1,'tag1':sample2,...}}}"""
	"""Usage:create_vcf_dict(vcffile)"""

	vcf_dict = {}

	with open(vcffile,'r') as f:	
		
                while True:
		        line = f.readline()
                        if line.startswith("##"):
                                continue
                        elif line.startswith("#"):
                                
                                head = line.lstrip("#").strip().split()[9:]
		                #Caculate the sample number in head
		                sample_num = len(head)
                                break

		for i in range(0,sample_num):
			locals()['tag' + str(i)] = head[i].strip('<').strip('>')
				
		while True:
			
			line_list = f.readline().strip().split()
			
			if not line_list:
				break
				
			ctg = line_list[0]
			pos = int(line_list[1])
			REF = line_list[3]
			ALT = line_list[4]
				
			if ctg in vcf_dict.keys():

				if pos not in vcf_dict[ctg].keys():
					vcf_dict[ctg][pos] = {'REF':REF,'ALT':ALT}	

					for i in range(0,sample_num):
						GT = line_list[i+9].split(':')[0].split('/')
				
						if GT[0] == '.' or GT[1] == '.':
							AD = ['-','-']
						else:
							AD = line_list[i+9].split(':')[1].split(',')
							
						vcf_dict[ctg][pos][locals()['tag' + str(i)]] = (GT,AD)
			
						
			else:
				vcf_dict[ctg] = {}
				vcf_dict[ctg][pos] = {'REF':REF,'ALT':ALT}
 
				for i in range(0,sample_num):
					GT = line_list[i+9].split(':')[0].split('/')
                                        if GT[0] == '.' or GT[1] == '.':
                                                 AD = ['-','-']
                                        else:
 
                                                 AD = line_list[i+9].split(':')[1].split(',')
 
                                        vcf_dict[ctg][pos][locals()['tag' + str(i)]] = (GT,AD)

	print('create vcf_dict done')
	return vcf_dict
	


def judge_snp(REF,ALT,GT,AD):
	
	"""Judge the base type is REF or ALT by GT and AD."""
	"""GT = ./. base_type = '-'"""
	"""GT = 1/1 base_type = ALT"""
	"""GT = 0/0 base_type = REF"""
	"""GT = 0/1 judge AD if AD[0] > AD[1] base_type = REF else base_type = ALT"""
	"""Usage:judge_snp(REF,ALT,GT,AD)"""

	def AD_compare(AD):
		
		'''Compare AC[0] and AC[1]'''
		if AD[0] > AD[1]:
			return True
		elif AD[0] < AD[1]:
			return False
	#Init base_type as -
	base_type = '-'
	
	if ('.') in GT:
		base_type = '-'

	elif GT[0] == '1':
		
		if GT[1] == '1':
			base_type = ALT
			
		elif GT[1] == '0':
			
			if AD_compare(AD):
				base_type = ALT
			else:
				base_type = REF
	elif GT[0] == '0':
		
		if GT[1] == '0':
			base_type = REF

		elif GT[1] == '1':
			
			if AD_compare(AD):
				base_type = REF
			else :
				base_type = ALT
	
	return base_type
	

def create_fasta_dict(infasta):
	
	"""Create a fasta dict {id:seq,...}"""
	"""Usage:create_fasta_dict(infasta)"""

	fasta_dict = {}
	with open(infasta,'r') as f:
		
		fasta = parse(f,'fasta')
		for record in fasta:
			
			fasta_dict[record.id] = str(record.seq)
	
	print('create fasta dict done')
	return fasta_dict
		

def  out_result(vcffile,output,m):
	
	"""
        
        """
	#Create the vcf dict
	vcf_dict = create_vcf_dict(vcffile)
	#Create the fasta dict
	#fasta_dict = create_fasta_dict(infasta)
	#Obtain the sample dict
	sample_dict = get_sample_dict(vcffile)
	#Obtain and sort the sample list
	sample_list = sorted(sample_dict.keys(),key=lambda x:int(x[3:]))
	
	sample_num = len(sample_list)

	#Out result with write in a file named out.matrix
	with open(output,'w') as o:
		
		head = 'CHROM\tPOS\tREF\t'
		for i in sample_list:
			head += sample_dict[i] + '\t'	
		
		o.write(head.rstrip('\t') + '\n')
		print('head write')

		chrom_list = sorted(vcf_dict.keys(),key=lambda x:int(x[3:][:-8]))

		for chrom in chrom_list:
                        for pos in sorted(vcf_dict[chrom].keys(),key=lambda x:int(x)):
			
				REF = vcf_dict[chrom][pos]["REF"]
					
				ow = '%s\t'*(3)%((chrom,pos,REF))
				
                                s = ''		
				for i in sample_list:
						
					GT = vcf_dict[chrom][pos][sample_dict[i]][0]
					AD = vcf_dict[chrom][pos][sample_dict[i]][1]
					ALT = vcf_dict[chrom][pos]['ALT']
					base_type = judge_snp(REF,ALT,GT,AD)	
					s = s + '%s\t'%(base_type)
				s = s.rstrip('\t')
    	     
				# Filter out if the missing rate is greater than m
				if s.split().count('-') < (sample_num * float(m)) :
					s = s + '\n'
                                        ows = ow + s
                                        o.write(ows)
                            
			print('%s done'%chrom)
		print('out matrix file done') 
        


def matrix2fasta(matrixfile,outfasta):

        """
        convert the snp matrix file to fasta
        """
        print("Running the matrix 2 fasta...")

        from Bio.SeqRecord import SeqRecord
        from Bio.Seq import Seq
        from Bio.SeqIO import write

        with open(outfasta,'w') as out:

                with open(matrixfile,'r') as f:

                        head = f.readline().split()[4:]
                        sample_num = len(head)
                        f_list = f.readlines()

                        for i in range(0,sample_num):
                                locals()['id' + str(i)] = head[i].strip('<').strip('>')
                                locals()['seq' + str(i)] = ''
                        print('Head read done')

                        print('Start')

                        for line in f_list:
                                line1 = line.split()[4:]
                                for i in range(0,sample_num):
                                        locals()['seq' + str(i)] = locals()['seq' + str(i)] + line1[i]

                        print('Read sequence done')

                        for i in range(0,sample_num):
#                               out.write(locals()['id' + str(i)] + '\n')
#                               out.write(locals()['seq' + str(i)] + '\n')
                                record = SeqRecord(Seq(locals()['seq' + str(i)]),
                                                id=locals()['id' + str(i)],
                                                description='')
                                write(record,out,'fasta')
                                print('Write %s done'%(locals()['id' + str(i)]))



				

if __name__ == '__main__':

        from optparse import OptionParser

        p = OptionParser(__doc__)
        p.add_option("-v","--vcf",dest="vcffile",
                      help="the vcf file of snp,input")
        p.add_option("-o","--outfasta",dest="outfasta",
                default="snp.fasta",help="the output file.[default:%default]")
        p.add_option("-m","--missing_rate",dest="missing_rate",
                default=0.4,help="the out put missing rate[default:%default]")
        
        opts,args = p.parse_args()

	if len(sys.argv) < 3:
		sys.exit(p.print_help())
		
        vcffile = opts.vcffile
	outfasta = opts.outfasta
        missing_rate = opts.missing_rate
        
        outmatrix = "out.matrix"
	out_result(vcffile,outmatrix,missing_rate)

        matrix2fasta(outmatrix,outfasta)

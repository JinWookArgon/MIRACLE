#!/usr/bin/env python

import logging

version_num = "0.1"
paras_default = {
		}

import os
import sys

import argparse
from MIRACLEpy.units import *
module_dir = os.path.dirname(__file__)
data_dir = os.path.join(module_dir, 'Data')

def args_process():
	commands = []
	commands_parser = {}
	parser = argparse.ArgumentParser(description=default_general['name'] + ": " + default_general["description"]
			)

	parser.usage = default_general['name'] + " [options]"
	parser.add_argument('-V', '--version', action='version', version=default_general['name'] + default_general['version'])
	parser.add_argument('-i', '--input', required=True, type=str, nargs=1, help='Input bam file xxx.bam [required]')
	parser.add_argument('-o', '--output', required=True, type=str, help='Output file name [required]')
	parser.add_argument('-b', '--bed', required=False, type=str, default=os.path.join(data_dir,"Invariable_Microsatellite_information.bed"), help='bed file format')
	parser.add_argument('-m', '--minimum', required=False, type=int, default=5, help='minimum length for microsatellites')
	parser.add_argument('-f', '--flanking', required=False, type=int, default=2, help='flanking region')
	parser.add_argument('-F', '--FDR', required=False, type=int, default=0.05, help='FDR value for significance')
	parser.add_argument('-r', '--read', required=False, type=int, default=6, help='minimum read count of matched microsatellite')
	parser.add_argument('-n', '--normal', required=False, type=str, default=os.path.join(data_dir,"Lengthlist_Reference_normal.txt"), help='matched normal summary file')
	parser.add_argument('-R', '--Random', required=False, type=int, default=0.8, help='the ratio of training set for random sampling')
	parser.add_argument('-M', '--Model', required=False, type=str,default=os.path.join(data_dir,"Training_data.txt"), help='Training_data_set')

	return parser.parse_args()


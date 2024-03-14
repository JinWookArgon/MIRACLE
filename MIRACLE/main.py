#!/usr/bin/env python3
import argparse
import sys
import os

curpath = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.append(os.path.dirname(curpath))

from MIRACLE.paras import *
from MIRACLE.length import *
from MIRACLE.model import *
from MIRACLE.statistics import *


def main():
	paras = args_process()
	if paras:
		paras_dict = vars(paras)
		for arg in paras_dict:
			print(f"{arg}: {paras_dict[arg]}")
		print(f"[step: 1] is started")
		save_length(paras)
		print(f"[step: 2] is started")
		count_below_threshold(paras)
		print(f"[step: 3] is started")
		test_new_samples(paras)
	pass

if __name__ == '__main__':
	main()
	print(f"Analysis is done!")
	pass


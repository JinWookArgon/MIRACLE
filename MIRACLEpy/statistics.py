import pandas as pd
from scipy.stats import ks_2samp
from statsmodels.stats.multitest import multipletests
import csv
import os

module_dir = os.path.dirname(__file__)
data_dir = os.path.join(module_dir, 'Data')

def safe_convert_to_float(x):
	try:
		return float(x)
	except ValueError:
		return None


def analyze_ks_fdr(input_file1,input_file2,file_prefix,read):
	
	output_file_ks = f"KSresult_{file_prefix}.txt"
	output_file_fdr = f"FDRresult_{file_prefix}.txt"
	
	data1 = pd.read_csv(input_file1, sep="\t")
	data2 = pd.read_csv(input_file2, sep="\t")
	
	x_data = [[safe_convert_to_float(item) for item in str(x).split(",") if item] for x in data1['repArray']]
	y_data = [[safe_convert_to_float(item) for item in str(y).split(",") if item] for y in data2['repArray']]

	filter_condition = [(len(x) >= read and len(y) >= read) for x, y in zip(x_data, y_data)]
	x_filtered = [x for x, condition in zip(x_data, filter_condition) if condition]
	y_filtered = [y for y, condition in zip(y_data, filter_condition) if condition]

	ks_results = [ks_2samp(x, y).pvalue for x, y in zip(x_filtered, y_filtered) if x and y]

	data1_filtered = data1.loc[filter_condition, ["index", "chr", "start", "end", "geneSymbol"]]
	output_data = pd.concat([data1_filtered.reset_index(drop=True), pd.DataFrame(ks_results, columns=['KS_p_value'])], axis=1)
	output_data.to_csv(output_file_ks, sep="\t", index=False, header=True, quoting=csv.QUOTE_MINIMAL)
	
	data3 = pd.read_csv(output_file_ks, sep="\t")
	fdr = multipletests(data3['KS_p_value'], method='fdr_bh')[1]
	fdr_results = pd.concat([data3.iloc[:, :5].reset_index(drop=True), pd.DataFrame(fdr, columns=['FDR_p_value'])], axis=1)
	
	fdr_results.to_csv(output_file_fdr, sep="\t", index=False, header=True, quoting=csv.QUOTE_MINIMAL)
	return output_file_fdr

def count_below_threshold(paras):
	input_file1 = "Lengthlist_" + paras.output + ".txt"
	if paras.normal != os.path.join(data_dir,'Lengthlist_Reference_normal.txt'):
		input_file2 = "Lengthlist_normal_" + paras.output + ".txt"
	else:
		input_file2 = paras.normal
	
	#print(f"input_file1: {input_file1}, input_file2: {input_file2}")
	file_prefix = paras.output
	read = paras.read
	FDR = paras.FDR
	output_file_fdr = analyze_ks_fdr(input_file1,input_file2,file_prefix,read)
	data = pd.read_csv(output_file_fdr, sep="\t")
	count=data.iloc[1:][data.iloc[1:]['FDR_p_value'] <= FDR].shape[0]
	header = "Case\tCounts\n";
	unstable_loci = f"{file_prefix}\t{count}"
	result = header + unstable_loci
	filename = f"Unstable_loci_count_{file_prefix}.txt"
	with open(filename, "w") as f:
		f.write(result)
	print(f"[step: 2] Statistical test is finished")

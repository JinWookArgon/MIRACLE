import sys
import pysam
import re
import time

start_time = time.time()

inputfile = sys.argv[1]

repeatno = 0
microsatellite = {}

with open("/Share/jwchoi/Data_SJL/hg38liftOver_minLen6_386384MS_WES_correction.bed") as data:
	print(f"reading bed file ..")
	for line in data:
		element = line.strip().split('\t')
		MS_chrom = element[0] 
		MS_start = int(element[1])
		MS_end = int(element[2])
		MS_Type = element[4]
		MS_Name = element[3]
		SEQ = element[5]
		MS_Flank1 = SEQ[3:5]
		MS_Flank2 = SEQ[-5:-3]
		if MS_Type == "mono":
			MS_Len = 1
		elif MS_Type == "di":
			MS_Len = 2
		elif MS_Type == "tri":
			MS_Len = 3
		elif MS_Type == "tetra":
			MS_Len = 4
		MS = SEQ[5: 5 + MS_Len]
		#if repeatno == 26455:
			#print(f"MS_Type: {MS_Type}")
		microsatellite[repeatno] = (MS_chrom, int(MS_start), int(MS_end), MS_Type, MS_Name, MS, MS_Flank1, MS_Flank2, MS_Len)
		repeatno += 1

lengths = {}
Save_read = {}
bam_file = pysam.AlignmentFile(inputfile, "rb")
print(f"reading bam file {inputfile} ..")
for repeatno, (chrom, start, end, MS_Type, MS_Name, MS, MS_Flank1, MS_Flank2, MS_Len) in microsatellite.items():
	#print(f"{repeatno}")
	for read in bam_file.fetch(chrom, start, end):
		#print(f"read name: {read.query_name}")
		read_seq = read.query_sequence
		read_start = read.reference_start
		read_MS_start = start - read_start
		i = 1
		repeat_length = 0
		#print(f"readID: {read.query_name}, readStart: {read.reference_start}, MSStart: {start}, read_seq: {read_seq[read_MS_start - 2 : read_MS_start]}, MS_Flank1: {MS_Flank1}")
		if read_seq[read_MS_start - 2 : read_MS_start] != MS_Flank1:
			continue
		#print(f"readID: {read.query_name}, readMSstart: {read_MS_start}, read_flank1: {read_seq[read_MS_start-2:read_MS_start]}, MS_Flank1: {MS_Flank1}")
		while True:
			remainder = i % MS_Len
			if remainder == 0:
				remainder = MS_Len
			if read_seq[read_MS_start  : read_MS_start + 1] == MS[remainder - 1 : remainder]:
				repeat_length += 1
			else:
				if read_seq[read_MS_start : read_MS_start + 2] == MS_Flank2:
					if repeatno in lengths:
						lengths[repeatno].append(repeat_length)
					else:
						lengths[repeatno] = [repeat_length]
						#print(f"MSno: {repeatno}, MS start: {start}, MS end: {end}, MS Flank1: {MS_Flank1}, MS: {MS}, MS Flank2: {MS_Flank2}, read ID: {read.query_name}, read start: {read_start}, length: {repeat_length}, read seq: {read_seq}")
					break
				else:
					break

			read_MS_start += 1
			i += 1

inputfile = inputfile.replace("./", "")
output_file = f"Summary_python_without_sputnik_{inputfile}"
time_file = f"Time_check_file"
#print(f"writing result in {output_file} ..")


with open(output_file, "w") as f:
	f.write("index\tchr\tstart\tend\tgeneSymbol\trepArray\n")
	for repeatno, repeat_info in microsatellite.items():
		MS_chrom, MS_start, MS_end, MS_Name = repeat_info[0], repeat_info[1], repeat_info[2], repeat_info[4]
		if repeatno in lengths:
			length_str = ",".join(map(str, lengths[repeatno]))
			f.write(f"{repeatno}\t{MS_chrom}\t{MS_start}\t{MS_end}\t{MS_Name}\t{length_str},\n")
		else:
			length_str = ""
			f.write(f"{repeatno}\t{MS_chrom}\t{MS_start}\t{MS_end}\t{MS_Name}\t{length_str}\n")

end_time = time.time()
execution_time = end_time - start_time

with open(time_file, "a") as time:
	time.write(f"{inputfile} running time: {execution_time:.6f} seconds\n")

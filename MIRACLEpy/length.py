import pysam
import os

module_dir = os.path.dirname(__file__)  
data_dir = os.path.join(module_dir, 'Data')

def parse_bed_file(BED, Flank):
	repeatno = 0
	microsatellite = {}
	with open(BED) as data:
		for line in data:
			element = line.strip().split('\t')
			MS_chrom = element[0] 
			MS_start = int(element[1])
			MS_end = int(element[2])
			MS_Type = element[4]
			MS_Name = element[3]
			SEQ = element[5]
			MS_Flank1 = SEQ[5-Flank:5]
			MS_Flank2 = SEQ[-5:-5+Flank]
			if MS_Type == "mono":
				MS_Len = 1
			elif MS_Type == "di":
				MS_Len = 2
			elif MS_Type == "tri":
				MS_Len = 3
			elif MS_Type == "tetra":
				MS_Len = 4
			MS = SEQ[5: 5 + MS_Len]
			microsatellite[repeatno] = (MS_chrom, int(MS_start), int(MS_end), MS_Type, MS_Name, MS, MS_Flank1, MS_Flank2, MS_Len)
			repeatno += 1
	return microsatellite

def process_bam_file(BED,BAM,microsatellite,Flank,MIN):
	lengths = {}
	bam_file = pysam.AlignmentFile(BAM, "rb")
	for repeatno, (chrom, start, end, MS_Type, MS_Name, MS, MS_Flank1, MS_Flank2, MS_Len) in microsatellite.items():
		for read in bam_file.fetch(chrom, start, end):
			read_seq = read.query_sequence
			read_start = read.reference_start
			read_MS_start = start - read_start
			i = 1
			repeat_length = 0
			if read_seq[read_MS_start - Flank : read_MS_start] != MS_Flank1:
				continue
			while True:
				remainder = i % MS_Len
				if remainder == 0:
					remainder = MS_Len
				if read_seq[read_MS_start  : read_MS_start + 1] == MS[remainder - 1 : remainder]:
					repeat_length += 1
				else:
					if read_seq[read_MS_start : read_MS_start + Flank] == MS_Flank2:
						if repeatno in lengths:
							if repeat_length >= MIN:
								lengths[repeatno].append(repeat_length)
						else:
							if repeat_length >= MIN:
								lengths[repeatno] = [repeat_length]
						break
					else:
						break
	
				read_MS_start += 1
				i += 1
	return lengths

def save_length(paras): 
	output_file = "Lengthlist_" + paras.output + ".txt"
	BED = paras.bed
	Flank = paras.flanking
	BAM = paras.input[0]
	MIN = paras.minimum
	microsatellite = parse_bed_file(BED,Flank)
	lengths = process_bam_file(BED,BAM,microsatellite,Flank,MIN)
	write_lengthlist_file(output_file,microsatellite,lengths)
	if paras.normal != os.path.join(data_dir, 'Lengthlist_Reference_normal.txt'):
		normal_file = paras.normal
		normal_lengths = process_bam_file(BED,normal_file,microsatellite,Flank,MIN)
		normal_output_file = "Lengthlist_normal_" + paras.output + ".txt"
		write_lengthlist_file(normal_output_file,microsatellite,normal_lengths)

def write_lengthlist_file(output_file, microsatellite, lengths):
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
	
	print(f"[step: 1] Measuring the length of microsatellite is finished.")

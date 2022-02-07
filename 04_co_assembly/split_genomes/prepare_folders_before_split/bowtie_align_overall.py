import json
import subprocess
import os
dirt_base = "/scratch/users/wzheng/Nextseq_04082019/genome_assembly_rerun/assembly/align/"
dirt_fastq = "/scratch/users/wzheng/Nextseq_04082019/genome_assembly_rerun/assembly/fastq_SE/"# dirt of SE fastq original files

with open(dirt_base + "cluster_members_assembly_final.json") as input:
	cluster_info = json.load(input)

for cluster_number in cluster_info.keys():
	temp_output_dirt = dirt_base+cluster_number + '/'
	os.mkdir(temp_output_dirt)
	subprocess.call("cp " + dirt_base + "original_fasta/"+ cluster_number + ".fasta " + temp_output_dirt, shell=True) 
	for barcode_temp in cluster_info[cluster_number]:
		subprocess.call("cp " + dirt_fastq + barcode_temp + ".fastq " + temp_output_dirt, shell=True) 	
	subprocess.call("sbatch -e " + cluster_number + '_align.err -o ' + str(cluster_number) + '_align.out ' + dirt_base + \
	'bowtie_align_cluster.sh ' + temp_output_dirt + ' ' + cluster_number, shell=True)

import pandas as pd
import scipy.spatial.distance as sdist
import os
import subprocess
import time
import json
from scipy.cluster.hierarchy import linkage, fcluster
dirt_base = "/scratch/users/wzheng/Nextseq_04082019/genome_assembly_rerun/assembly/" # a base dirt
dirt_fastq = dirt_base + "fastq_SE/"# dirt of SE fastq original files
dirt_csv_dirt = dirt_base + "round_1/round_2_inconsistent/"#dirt of compare file
out_put_dirt = dirt_base + "round_1/round_2_inconsistent/round_3/"#dirt of output dirt, including cated fastq, assembly, and fasta files
temp_work_dirt = dirt_base + "round_1/round_2_inconsistent/round_3/temp/"# temp dirt used to cat fastq files
file_name = '2nd_round_cmp.csv'

mat_file = pd.read_csv(dirt_csv_dirt+file_name)
mat_file = 1.0-mat_file
for i in range(len(mat_file)):
        mat_file.iloc[i][i] = 0


square_form = sdist.squareform(mat_file)
assignments = fcluster(linkage(square_form, method = 'complete'), 0.95)
print(max(assignments))
cluster_result = {}
for j in range(max(assignments)):
        a_temp_list = []
        for i in range(len(assignments)):
                if assignments[i] == j+1:
                        a_temp_list += [mat_file.columns.values[i][:-len('.fasta')]]
        cluster_result[str(j)]=a_temp_list
with open(out_put_dirt+'cluster_members_'+file_name[:3]+'.json', 'w') as out:
        json.dump(cluster_result, out)
with open(dirt_csv_dirt + 'cluster_members_1st.json') as input:
        cluster_result_readin = json.load(input)

for j in range(max(assignments)):
        a_temp_list = []
        for i in range(len(assignments)):
                if assignments[i] == j+1:
                        a_temp_list += [mat_file.columns.values[i]]
        a_temp_list_of_barcode = []
        for i in a_temp_list:
                for k in cluster_result_readin[i[:-len('.fasta')]]:
                        a_temp_list_of_barcode += [k]
        for BC_temp in a_temp_list_of_barcode:
               # BC_temp = BC_temp_with_fastq[:-len(".fastq")]
                subprocess.call("cp " + dirt_fastq + BC_temp + ".fastq " + temp_work_dirt, shell=True)
        subprocess.call("cat " + temp_work_dirt +"*.fastq > " + out_put_dirt + str(j) + '.fastq', shell=True)
        subprocess.call("rm " + temp_work_dirt +"*.fastq", shell=True)
        subprocess.call("sbatch -o " + out_put_dirt + str(j) + ".spades.out.txt " + dirt_base + \
"spades_sc_assembly.sh " + str(j) + " " + out_put_dirt, shell = True)
# spades_sc_assembly.sh take 2 varialbes, 1st is barcode name, 2nd is the dirt to this fastq which
# is also the file



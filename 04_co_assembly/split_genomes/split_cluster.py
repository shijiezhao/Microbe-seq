import json
import subprocess
import os
import pandas as pd
import numpy as np
import math
import random
import sys
folder_name = sys.argv[1] # folder name, [0] is this py file
folder_name = str(folder_name)
print(folder_name)
dirt_common = "/scratch/users/wzheng/Nextseq_04082019/genome_assembly_rerun/assembly/align/" # this is to be changed, all initial cluster folders are here
dirt_final_fasta_output = "/scratch/users/wzheng/Nextseq_04082019/genome_assembly_rerun/assembly/align/fasta_after_split/"

if len(folder_name.split('_')) != 1:
    dirt_base = dirt_common + 'split_output_dirt/' + folder_name + '/'
else:
    dirt_base = dirt_common + folder_name + '/' 
# parameters that can be changed
cutoff_of_contig = 1000 # contigs less than this number will be removed from analysis
minimum_cell_number= 10 # clusters of cells with no more than this number of barcodes are removed
minimum_cell_removal = 3 # if no more than this number of cells are removed from previous previous bin, stop further process
cell_kept_ratio_cutoff = float(0.6) # if less than this number of cells are kept after split, stop process

print("Each round's name is the working folder name. All folders are in the root folder. 201_0 means the 1st branch from round1, 201_1_0_1 means the round3 2nd cluster from round2 1st cluster from round1 2nd cluster.\n")
print("This is round {}.".format(len(folder_name.split('_'))-1))

# function read_coverage_file_parse
# dirtectory of read_coverage files, it must have 1 file which is the assembly, ending with ".fasta"
# output, a dataframe self_mapping_df, each row is a contig, each column is a barcode or basic information
def read_coverage_file_parse(temp_working_dirt):
    file_list = os.listdir(temp_working_dirt)
    list_of_barcodes = []
    for file_temp in file_list:
        if '.fasta' in file_temp:
            assembly_file_name = file_temp
        if ".read_coverage" in file_temp and file_temp[:-len(".read_coverage")].isdigit():
            list_of_barcodes += [file_temp[:-len(".read_coverage")]]
                
    contig_index_list = []
    contig_length_list = []
    contig_coverage_list = []
    with open(temp_working_dirt+assembly_file_name) as finput:
        while True:
            line_read = finput.readline()  
            if len (line_read) == 0:
                break
            if ">" in line_read: 
                line_split_temp = line_read.split("_")
                contig_index_list +=[int(line_split_temp[1])]
                contig_length_list +=[int(line_split_temp[3])]    
                contig_coverage_list +=[float(line_split_temp[5])]                  
    self_mapping_df = pd.DataFrame({'contig_index': contig_index_list}) 
    self_mapping_df['contig_length'] = contig_length_list
    self_mapping_df['contig_coverage'] = contig_coverage_list
    contig_count_pd = [0] * len(contig_index_list)#[ [] for i in range(len(contig_index_list)) ]                
    for i in list_of_barcodes:
        BC_temp = str(i)
        column_name_temp = "BC_"+ BC_temp
        bam_read_count = pd.read_csv(temp_working_dirt+BC_temp+".read_coverage",sep='\t', header=None)
        bam_read_count.columns = ['contig', 'length', 'read_count','unpaired']
        contig_list_temp = list(set(bam_read_count.contig))
        #for i in range(len(contig_count_pd)):
         #   contig_count_pd[i] = bam_read_count.iloc[i]['read_count']
        #self_mapping_df[column_name_temp] = contig_count_pd
        self_mapping_df[column_name_temp] = list(bam_read_count['read_count'])[:-1]
    # remove contigs that are less than 1000bp
    to_remove_list = []
    for i in range(len(self_mapping_df)):
        if self_mapping_df['contig_length'][i] < cutoff_of_contig:
            to_remove_list += [i]
    self_mapping_df = self_mapping_df.drop(to_remove_list)
    if len(self_mapping_df) <= 1:# if assembly contigs are all less than specified length, or only 1 is longer, stop process
	subprocess.call("cp " + temp_working_dirt + "*.fasta " + dirt_final_fasta_output, shell = True)
	return(0)
    self_mapping_df.to_csv(temp_working_dirt+'/self_mapping_df.csv',index=False)
    return(1)
    #return(self_mapping_df)

# function cluster_contig
# use binary clustering to classify contigs, only keep contigs in the large clade
# Thenr use this clustering to bin clean cells and use these cells to re assemble
# input is the directory and parsed read_coverage dataframe

def cluster_contig_cleanup(temp_working_dirt):
    self_mapping_df = pd.read_csv(temp_working_dirt+'/self_mapping_df.csv')
    self_mapping_df_temp = self_mapping_df
    self_mapping_df_temp = self_mapping_df_temp.drop(['contig_index', 'contig_length', 'contig_coverage'], axis=1)
    median_list_temp = list(self_mapping_df_temp.median(axis=1))
    for i in range(len(self_mapping_df_temp)):
        for j in range(len(self_mapping_df_temp.iloc[i])):
            if self_mapping_df_temp.iloc[i][j]>median_list_temp[i]:
                self_mapping_df_temp.iloc[i][j] = 1
            else:
                self_mapping_df_temp.iloc[i][j] = 0
    # This is to culster contigs by mapping of each barcodes, with 'ward' method
    from scipy.cluster.hierarchy import dendrogram, linkage, cut_tree
    from matplotlib import pyplot as plt
    list_to_cluster = range(self_mapping_df_temp.shape[0])
    linked = linkage(self_mapping_df_temp, 'ward')
    cluster_number = 2
    cutree_contigs = cut_tree(linked, n_clusters=cluster_number)
    group_1_length = 0
    group_2_length = 0
    for i in range(len(cutree_contigs)):
        if cutree_contigs[i] == 0:
            group_1_length += self_mapping_df.iloc[i].contig_length
        else:
            group_2_length += self_mapping_df.iloc[i].contig_length
    print "Total contig length is {}, group 0 length is {}, group 1 length is {}.\n".    format(group_1_length+group_2_length, group_1_length, group_2_length)
    
    # below is to use cluster information to select cells
    self_mapping_df_temp = self_mapping_df.copy()
    self_mapping_df_temp = self_mapping_df_temp.drop(['contig_index', 'contig_length', 'contig_coverage'], axis=1)
    self_mapping_df_temp = self_mapping_df_temp.T
    self_mapping_df_temp['total_of_each_cell']=self_mapping_df_temp.sum(axis=1)
    for i in range(cluster_number):
        index_of_this_cluster = [] 
        for j in range(len(cutree_contigs)):
            if cutree_contigs[j] == i:
                index_of_this_cluster += [j]
        self_mapping_df_temp['hierarchy_cluster_'+str(i)]=        self_mapping_df_temp[self_mapping_df_temp.columns.values[index_of_this_cluster]].sum(axis=1)
    
    BC_list_0_temp = list(self_mapping_df_temp.loc                                  [self_mapping_df_temp['hierarchy_cluster_'+str(0)]          /(self_mapping_df_temp.total_of_each_cell)>0.95].index)
    BC_list_1_temp = list(self_mapping_df_temp.loc                                  [self_mapping_df_temp['hierarchy_cluster_'+str(1)]          /(self_mapping_df_temp.total_of_each_cell)>0.95].index)
    BC_list_not_clean_temp = len(self_mapping_df_temp)-len(BC_list_0_temp)-len(BC_list_1_temp)

    print "Total cell number is {}, group 0 cell number is {}, group 1 cell nubmer is {}. \n".    format(len(self_mapping_df_temp), len(BC_list_0_temp), len(BC_list_1_temp))
    if len(BC_list_0_temp) + len(BC_list_1_temp) < cell_kept_ratio_cutoff * len(self_mapping_df_temp) and folder_name not in ['77_1', '270', '76_0', '78_0_1', '215', '271']:
# if too many cells are removed, stop
# The list of folders are more than 10% contamination after stop, thus keep cleaning 
# 202_0 and 109_1 both are more than 10% contaminated, however, there is less than 3 cells in all sub bins, so they are not used:# too many cells removed, stop
        print "Too many cells removed, stop.\n"
	subprocess.call("cp " + temp_working_dirt + "*.fasta " + dirt_final_fasta_output, shell = True)
        return
    if len(BC_list_0_temp) == len(self_mapping_df_temp) or len(BC_list_1_temp) == len(self_mapping_df_temp):
        print "No cell change to clusters, stop.\n"
	subprocess.call("cp " + temp_working_dirt + "*.fasta " + dirt_final_fasta_output, shell = True)
        return   
    flag_next_process = 0
    if len(BC_list_0_temp) > minimum_cell_number and len(self_mapping_df_temp) - len(BC_list_0_temp) > minimum_cell_removal:# if too few cell, stop
	flag_next_process = 1	
        prepare_folder(dirt_base,0,BC_list_0_temp) # each item in BC_list is BC_XXXXXXX
    if len(BC_list_1_temp) > minimum_cell_number and len(self_mapping_df_temp) - len(BC_list_1_temp) > minimum_cell_removal:
	flag_next_process = 1
        prepare_folder(dirt_base,1,BC_list_1_temp)    
    if flag_next_process == 0:# means both branches are not qualified for next step
	subprocess.call("cp " + temp_working_dirt + "*.fasta " + dirt_final_fasta_output, shell = True)

# function prepare_folder
# takes folder directory and list of barcode_names
# Moves fastq files from previous folder, then
    #1. Cat all fastq files into 1 and assemble 
    #2. Align each fastq to reference file to generate sam files
    #3. Transfer sam files to read_coverage files
    #4. Sbatch a job with the new folder as input
def prepare_folder(fastq_source, cluster_number, BC_list):
    folder_name_temp = folder_name + '_' + str(cluster_number)
    new_folder_dirt = dirt_common + 'split_output_dirt/' + folder_name_temp + '/'
    os.mkdir(new_folder_dirt)
    for barcode_temp in BC_list:        
        subprocess.call("cp " + fastq_source + barcode_temp[3:] + ".fastq " + new_folder_dirt, shell=True)
    subprocess.call("cat " + new_folder_dirt +"*.fastq > " + new_folder_dirt + 'total.fastq', shell=True)
    subprocess.call('spades.py --sc --careful --pe1-s ' + new_folder_dirt + 'total.fastq ' +                    '-o ' + new_folder_dirt + 'total_scCareful', shell=True)
    subprocess.call('rm ' + new_folder_dirt + 'total.fastq', shell=True)
    subprocess.call('mv ' +  new_folder_dirt + 'total_scCareful/contigs.fasta '+                     new_folder_dirt + str(folder_name_temp) + '.fasta', shell=True)
    subprocess.call('rm -r ' +  new_folder_dirt + 'total_scCareful/', shell=True)
    subprocess.call('bowtie2-build ' + new_folder_dirt + str(folder_name_temp) + '.fasta ' +                     new_folder_dirt + str(folder_name_temp) + '_reference', shell=True)
    for i in range(len(BC_list)):
        barcode_temp = BC_list[i][3:]
        subprocess.call('bowtie2 -x ' + new_folder_dirt + str(folder_name_temp) + '_reference '                         + '-U ' + new_folder_dirt + barcode_temp + ".fastq -S " +                         new_folder_dirt + barcode_temp + ".sam", shell=True)
        subprocess.call("/scratch/users/wzheng/bin/samtools-1.9/samtools sort " + new_folder_dirt + barcode_temp + ".sam > " +                         new_folder_dirt + barcode_temp + ".bam", shell=True)
        subprocess.call("/scratch/users/wzheng/bin/samtools-1.9/samtools index " + new_folder_dirt + barcode_temp + ".bam", shell=True)
        subprocess.call("/scratch/users/wzheng/bin/samtools-1.9/samtools idxstats " + new_folder_dirt + barcode_temp + ".bam > "                         + new_folder_dirt + barcode_temp + ".read_coverage", shell=True)
        subprocess.call('rm ' + new_folder_dirt + barcode_temp + ".sam", shell=True)
    subprocess.call('sbatch -e ' + dirt_common +'split_err_out_files/' + folder_name_temp + '_%j.split.err ' + '-o ' + dirt_common +'split_err_out_files/' + folder_name_temp + '_%j.split.out ' + dirt_common + 'split_cluster.sh ' + folder_name_temp, shell=True)

flag_if_no_large_cluster = read_coverage_file_parse(dirt_base)
if flag_if_no_large_cluster == 0:
    print("Assemly too small, less than 2 contigs larger then specified length.")
else:
    cluster_contig_cleanup(dirt_base)


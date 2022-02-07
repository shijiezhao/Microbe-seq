#!/usr/bin/env python3
# Converting Bowtie2 depths to a tsv file
#   stdin   Bowtie2 depth line
#   stdout  TSV rows. The columns are contig names, total depth, average depth
import sys
import fileinput

result = {}

for line in fileinput.input():
    row = line.split('\t')
    result[row[0]] = int(row[2]) + (0 if row[0] not in result else result[row[0]])

for contig in result:
    length = int(contig.split('length_')[-1].split('_')[0])
    val = length/float(result[contig])
    sys.stdout.write(contig + '\t' + str(result[contig]) + '\t' + str(val) + '\n')


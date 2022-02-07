#!/bin/bash
#SBATCH -N 1
#SBATCH -n 16
#SBATCH --time=48:00:00
#SBATCH --mem=20480
#SBATCH -p defq
# variable 1 is barcode name, variable 2 is output dirt, variable 3 is input dirt
# this is specific for round 1 assembly where var2 and var3 are different
# other rounds they should be the same

module load c3ddb/SPAdes/3.13.0
spades.py --sc --careful --pe1-s ${3}${1}.fastq -o ${2}${1}_scCareful
#rm ${2}${1}.fastq
mv ${2}${1}_scCareful/contigs.fasta ${2}${1}.fasta
rm -r ${2}${1}_scCareful

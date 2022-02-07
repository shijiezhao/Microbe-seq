#!/bin/bash
#SBATCH -N 1
#SBATCH -n 16
#SBATCH --time=48:00:00
#SBATCH --mem=51200
#SBATCH -p defq

module load c3ddb/SPAdes/3.13.0
spades.py --sc --careful --pe1-s ${2}${1}.fastq -o ${2}${1}_scCareful
#rm ${2}${1}.fastq
mv ${2}${1}_scCareful/contigs.fasta ${2}${1}.fasta
rm -r ${2}${1}_scCareful

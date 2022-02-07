#!/bin/bash
#SBATCH -N 1
#SBATCH -n 16
#SBATCH --time=9:59:59
#SBATCH --exclusive  
#SBATCH --mem=102400
#SBATCH -p sched_mem1TB_centos7

# at terminal, run below, it is for trimmed metagenome-like datasets
# for file_temp in *_trimmed.fastq; do
# echo ${file_temp}
# sbatch -e ${file_temp/.fastq/}.kraken2.standard.err -o ${file_temp/.fastq/}.kraken2.standard.out kraken2_run_04282019.sh ${file_temp/.fastq/}
# done


{dirt_to_Kraken2} --db {dirt_to_Kraken2_standard_reference} --threads 16 --fastq-input ${1}.fastq --output ${1}.kraken2.standard.taxa

#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --time=5:00:00
#SBATCH --mem=4096
#SBATCH -p defq

## This file takes dirt as variable 1 and fasta file number as variable 2
## The result is to align each fastq SE file to fasta reference, and use samtools to convert it to depth and coverage count files

dirt=${1}
number=${2}
module load c3ddb/bowtie2/2.2.6

bowtie2-build ${dirt}${number}.fasta ${dirt}${number}_reference 

for FILE in ${dirt}*.fastq; do
sbatch -e ${FILE/.fastq/}.err.txt -o ${FILE/.fastq/}.out.txt \
/scratch/users/wzheng/Nextseq_04082019/genome_assembly_rerun/assembly/align/bowtie_align.sh ${dirt}${number}_reference ${FILE}
sleep 1
done


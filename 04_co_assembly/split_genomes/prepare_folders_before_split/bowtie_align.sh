#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --time=2:00:00
#SBATCH --mem=4096
#SBATCH -p defq
## This file takes reference file as variable 1 and fastq file and variable 2


module load c3ddb/bowtie2/2.2.6
bowtie2 -x ${1} -U ${2} -S ${2/.fastq/}.sam 

module load c3ddb/samtools/1.6
module load c3ddb/xz/5.2.3
dirt_num=${2/.fastq/}
samtools sort ${dirt_num}.sam > ${dirt_num}.bam
samtools depth ${dirt_num}.bam | python \
/scratch/users/wzheng/Nextseq_04082019/genome_assembly_rerun/assembly/align/depth-tsv.py > ${dirt_num}.tsv
samtools index ${dirt_num}.bam
samtools idxstats ${dirt_num}.bam > ${dirt_num}.read_coverage

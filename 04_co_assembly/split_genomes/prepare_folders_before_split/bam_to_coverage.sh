#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --time=2:00:00
#SBATCH --mem=2048
#SBATCH -p defq

## variable is bam file without ".bam"

module load c3ddb/samtools/1.6
samtools index ${1}.bam
samtools idxstats ${1}.bam > ${1}.read_coverage

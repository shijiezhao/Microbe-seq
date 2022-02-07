#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --time=10:00:00
#SBATCH --mem=2048
#SBATCH -p defq
#SBATCH -e bam_to_coverage_overall_%j.err
#SBATCH -o bam_to_coverage_overall_%j.out

for file in */*.bam; do
sbatch -e ${file/.bam/}.bam_to_coverage.err -o ${file/.bam/}.bam_to_coverage.out bam_to_coverage.sh ${file/.bam/}
sleep 0.2
done


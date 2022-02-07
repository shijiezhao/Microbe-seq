#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --time=35:00:00
#SBATCH --mem=4096
#SBATCH -p defq
#SBATCH -e assembly_round1_%j.err
#SBATCH -o assembly_round1_%j.out

#cd /scratch/users/wzheng/Nextseq_04082019/genome_assembly_rerun/assembly/fastq_SE
cd /scratch/users/wzheng/Nextseq_04082019/genome_assembly_rerun/assembly/round_1/fastq_SE_temp
for FILE in *.fastq; do
sbatch -o /scratch/users/wzheng/Nextseq_04082019/genome_assembly_rerun/assembly/round_1/${FILE/.fastq/}_%j.spades.out.txt \
/scratch/users/wzheng/Nextseq_04082019/genome_assembly_rerun/assembly/spades_sc_assembly_round_1.sh ${FILE/.fastq/} \
/scratch/users/wzheng/Nextseq_04082019/genome_assembly_rerun/assembly/round_1/ \
/scratch/users/wzheng/Nextseq_04082019/genome_assembly_rerun/assembly/fastq_SE/
sleep 0.1
done


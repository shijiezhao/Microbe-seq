#!/bin/bash
#SBATCH -N 1
#SBATCH -n 16
#SBATCH --time=72:00:00
#SBATCH --mem=51200
#SBATCH -p defq

# run following at terminal
# for dirt in {0..363}; do
# sbatch -e /scratch/users/wzheng/Nextseq_04082019/genome_assembly_rerun/assembly/align/split_err_out_files/${dirt}_%j.split.err \
# -o /scratch/users/wzheng/Nextseq_04082019/genome_assembly_rerun/assembly/align/split_err_out_files/${dirt}_%j.split.out \
# /scratch/users/wzheng/Nextseq_04082019/genome_assembly_rerun/assembly/align/split_cluster.sh ${dirt}
# done
module load c3ddb/bowtie2/2.2.6
#module load c3ddb/samtools/1.6
module load c3ddb/SPAdes/3.13.0
module load c3ddb/xz/5.2.3

python split_cluster.py ${1}


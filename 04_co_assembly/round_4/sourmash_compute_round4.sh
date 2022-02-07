#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --time=21:30:00
#SBATCH --mem=2048
#SBATCH -p defq
#SBATCH -e sourmash_compute_round4_%j.err.txt
#SBATCH -o sourmash_compute_round4_%j.out.txt

for FILE in *.fasta; do
sbatch -e ${FILE/.fasta/}.err.txt -o ${FILE/.fasta/}.out.txt sourmash_compute.sh ${FILE/.fasta/}
sleep 0.5
done

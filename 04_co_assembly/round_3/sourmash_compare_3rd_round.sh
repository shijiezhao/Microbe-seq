#!/bin/bash
#SBATCH -N 1
#SBATCH -n 16
#SBATCH --time=50:30:00
#SBATCH --mem=249999
#SBATCH -p defq
#SBATCH -o sourmash_compare_3rdRound_%j.out.txt
#SBATCH -e sourmash_compare_3rdRound_%j.err.txt

#conda activate
source activate smash
sourmash compare *.sig -k 51 -o 3rd_round_cmp.npy --csv 3rd_round_cmp.csv

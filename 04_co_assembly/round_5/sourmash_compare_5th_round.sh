#!/bin/bash
#SBATCH -N 1
#SBATCH -n 8
#SBATCH --time=5:30:00
#SBATCH --mem=10240
#SBATCH -p defq
#SBATCH -o sourmash_compare_5thRound_%j.out.txt
#SBATCH -e sourmash_compare_5thRound_%j.err.txt

#conda activate
source activate smash
sourmash compare *.sig -k 51 -o 5th_round_cmp.npy --csv 5th_round_cmp.csv

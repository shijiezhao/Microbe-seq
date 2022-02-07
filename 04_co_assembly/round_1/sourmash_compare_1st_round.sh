#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --time=30:30:00
#SBATCH --mem=209999
#SBATCH -p defq
#SBATCH -o sourmash_compare_1stRound.out.txt
#SBATCH -e sourmash_compare_1stRound.err.txt

conda activate
source activate smash
sourmash compare *.sig -k 51 -o 1st_round_cmp.npy --csv 1st_round_cmp.csv

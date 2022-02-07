#!/bin/bash
#SBATCH -N 1
#SBATCH -n 8
#SBATCH --time=50:30:00
#SBATCH --mem=51200
#SBATCH -p defq
#SBATCH -o sourmash_compare_4thRound_%j.out.txt
#SBATCH -e sourmash_compare_4thRound_%j.err.txt

#conda activate
source activate smash
sourmash compare *.sig -k 51 -o 4th_round_cmp.npy --csv 4th_round_cmp.csv

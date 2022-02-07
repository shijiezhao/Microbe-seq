#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --time=50:30:00
#SBATCH --mem=499999
#SBATCH -p sched_mem1TB_centos7
#SBATCH -o sourmash_compare_2ndRound_%j.out.txt
#SBATCH -e sourmash_compare_2ndRound_%j.err.txt

#conda activate
source activate smash
sourmash compare *.sig -k 51 -o 2nd_round_cmp.npy --csv 2nd_round_cmp.csv

#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --time=5:00:00
#SBATCH --mem=2048
#SBATCH -p defq
#SBATCH -e bowtie_align_overall_%j.err
#SBATCH -o bowtie_align_overall_%j.out

python bowtie_align_overall.py


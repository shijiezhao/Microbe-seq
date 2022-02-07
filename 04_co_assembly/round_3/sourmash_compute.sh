#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --time=05:30:00
#SBATCH --mem=5120
#SBATCH -p defq

#conda activate
source activate smash
sourmash compute --track-abundance ${1}.fasta --output ${1}.sig

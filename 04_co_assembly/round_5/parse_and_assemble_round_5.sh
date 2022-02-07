#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --time=10:30:00
#SBATCH --mem=10000
#SBATCH -p defq
#SBATCH -o parse_and_assemble_round5_%j.out.txt
#SBATCH -e parse_and_assemble_round5_%j.err.txt

python parse_ComparedFile_assemble_round5.py

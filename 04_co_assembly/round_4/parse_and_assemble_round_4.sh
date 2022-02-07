#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --time=50:30:00
#SBATCH --mem=50000
#SBATCH -p defq
#SBATCH -o parse_and_assemble_round4_%j.out.txt
#SBATCH -e parse_and_assemble_round4_%j.err.txt

python parse_ComparedFile_assemble_round4.py

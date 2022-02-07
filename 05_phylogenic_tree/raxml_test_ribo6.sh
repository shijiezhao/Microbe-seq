#!/bin/bash
#SBATCH -N 1
#SBATCH -n 32
#SBATCH --time=48:00:00
#SBATCH --mem=10240
#SBATCH -p defq
#SBATCH -e raxml_%j.err
#SBATCH -o raxml_%j.out

raxmlHPC-PTHREADS -T 32 -f a -m PROTGAMMALG -p 12345 -x 12345 -# 100 -s concatenated-proteins_Bacteria_71_ribosomal38.fa -n ribos38_boot100

#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --time=24:00:00
#SBATCH --mem=10240
#SBATCH -p sched_mem1TB_centos7
#SBATCH -e anvio_contig_%j.err
#SBATCH -o anvio_contig_%j.out

#conda activate anvio-6.1
for FILE in *.fa; do
anvi-script-FASTA-to-contigs-db ${FILE}
done

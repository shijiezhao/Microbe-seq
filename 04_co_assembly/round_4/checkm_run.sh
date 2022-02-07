#!/bin/bash
#SBATCH -N 1
#SBATCH -n 32
#SBATCH --time=96:00:00
#SBATCH --mem=51200
#SBATCH -p defq
#SBATCH -e checkm_run_%j.err
#SBATCH -o checkm_run_%j.out

checkm lineage_wf -t 32 for_checkm/ for_checkm/checkm_lineage_wf
checkm qa for_checkm/checkm_lineage_wf/lineage.ms for_checkm/checkm_lineage_wf/ \
> for_checkm/checkm_lineage_wf/qa_results

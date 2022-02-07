#!/bin/bash
#SBATCH -N 1
#SBATCH -n 16
#SBATCH --time=25:00:00
#SBATCH --mem=10240
#SBATCH -p sched_mem1TB_centos7
#SBATCH -e variant_call_err_%j.txt
#SBATCH -o variant_call_out_%j.txt

# ${1} is the assembled genome name
# should sbumit this order at the folder of interest
module load c3ddb/xz/5.2.3

/scratch/users/wzheng/bin/bcftools-1.9/bin/bcftools mpileup -f ${1} -a FORMAT/AD *.bam > variants/raw_calls.bcf
/scratch/users/wzheng/bin/bcftools-1.9/bin/bcftools call --ploidy 1 -v -m variants/raw_calls.bcf > variants/calls.vcf
/scratch/users/wzheng/bin/bcftools-1.9/bin/bcftools view -v snps variants/calls.vcf > variants/calls_snps.vcf
/scratch/users/wzheng/bin/bcftools-1.9/bin/bcftools filter -o variants/calls_snps_qual30.vcf -i '%QUAL>30' variants/calls_snps.vcf


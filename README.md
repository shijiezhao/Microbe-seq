# Microbe-seq
Single-cell genomic sequencing of the human gut microbiome
Codes and intermediary files for reproducing figures from “High-throughput, single-microbe genomics with strain resolution, applied to a human gut microbiome”, by Shijie Zhao and Wenshan Zheng. (co-first authors). We will provide the exact link for the manuscript when it’s available from the journal.

01_sort_SAGs.ipynb preprocesses raw sequencing data into individual SAGs.
02_mock_alignment contains command line scripts for aligning SAGs from a mock community to the reference genomes. Related to Figure 1 and S2.
03_kraken_standard.sh and 03_kraken_yeast.sh are used to do metagenomics and pooled SAGs taxonomy assignment. Related to Figure S3 and S4.
04_co_assembly contains scripts used for iterative clustering of SAGs from the same species and co-assembly. Related to Figure 2.
05_phylogenic_tree contains phylogenetic tree from the 76 species. Related to Figure 2.
06_strain_calling splits SAGs from different strains from the same species. Related to Figure 3, S8, S9, and S10.
07_HGT.ipynb is used for HGT detection between high-quality strain-resolved genomes. Related to Figure 4.
08_HGT_QC.ipynb checks HGT events quality. Related to Figure S11 and S12.
09_Bias_evaluation.ipynb compares species-level methodological biases between single-cell and metagenomics. Related to Figure S5 and S6.

# Microbe-seq

## Overview
This repository contains the code and intermediary files for reproducing figures from the manuscript titled "High-throughput, single-microbe genomics with strain resolution, applied to a human gut microbiome," authored by Shijie Zhao and Wenshan Zheng (co-first authors). The link to the manuscript will be provided once it is available from the journal.

## Repository Structure
Each directory contains specific scripts related to different figures and analyses described in the manuscript:

### 01_sort_SAGs.ipynb
- **Purpose**: Preprocesses raw sequencing data into individual Single Amplified Genomes (SAGs).

### 02_mock_alignment
- **Contents**: Command line scripts for aligning SAGs from a mock community to reference genomes.
- **Related Figures**: Figure 1, Supplementary Figure S2.

### 03_kraken_standard.sh and 03_kraken_yeast.sh
- **Function**: Perform metagenomics and pooled SAGs taxonomy assignments.
- **Related Figures**: Supplementary Figures S3 and S4.

### 04_co_assembly
- **Description**: Contains scripts used for iterative clustering of SAGs from the same species and co-assembly.
- **Related Figures**: Figure 2.

### 05_phylogenic_tree
- **Contents**: Scripts for constructing phylogenetic trees from the 76 species.
- **Related Figures**: Figure 2.

### 06_strain_calling
- **Purpose**: Splits SAGs from different strains of the same species.
- **Related Figures**: Figure 3, Supplementary Figures S8, S9, and S10.

### 07_HGT.ipynb
- **Function**: Used for Horizontal Gene Transfer (HGT) detection between high-quality strain-resolved genomes.
- **Related Figures**: Figure 4.

### 08_HGT_QC.ipynb
- **Description**: Checks the quality of HGT events.
- **Related Figures**: Supplementary Figures S11 and S12.

### 09_Bias_evaluation.ipynb
- **Purpose**: Compares species-level methodological biases between single-cell and metagenomic approaches.
- **Related Figures**: Supplementary Figures S5 and S6.

### genome_coassemblies
- **Contents**: Includes all species-level and strain-level genome co-assemblies.
- **Note**: ID corresponds to the bin ID in Table S3.

## Access and Usage
To reproduce the results and figures, clone this repository and follow the instructions within each script or notebook.

## Contact
For further information or issues, please contact the repository administrators or open an issue in this GitHub repository.

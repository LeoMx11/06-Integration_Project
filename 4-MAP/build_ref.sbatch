#!/bin/bash
#SBATCH --job-name=build_ref
#SBATCH --partition=batch
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --time=24:00:00
#SBATCH --output=build_ref_%j.log
#SBATCH --error=build_ref_%j.err
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=leomcmahon@ucsb.edu  # optional

source ~/.bashrc
conda activate rsem_env

cd /home/leomcmahon/06-Integration_Project/4-MAP

rm -rf reference
mkdir reference

rsem-prepare-reference \
  --star \
  --gtf bs_primary_asm.gtf \
  bs_primary_asm.fa \
  reference/reference


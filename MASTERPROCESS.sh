#!/bin/bash

# Arguments
USER_ID=$1

# Safety checks
if [ -z "$USER_ID" ]; then
  echo "Usage: $0 <USER_ID>"
  exit 1
fi

source ~/miniconda3/etc/profile.d/conda.sh

# Trimmomatic

conda env create -f /home/${USER_ID}/06-Integration_Project-main/2-Conda_envs/trimmo.yml
conda activate trimmo
echo "Starting trimmomatic at: $(date)"
python3 /home/${USER_ID}/06-Integration_Project-main/3-TRIM/MASTERPROCESS_trimmomatic.py ${USER_ID}
echo "Finished trimmomatic at: $(date)"
conda deactivate

# Create reference for rsem/star

conda env create -f /home/${USER_ID}/06-Integration_Project-main/2-Conda_envs/rsem_env.yml
conda activate rsem_env
cd /home/${USER_ID}/06-Integration_Project-main/4-MAP
rm -rf reference
mkdir reference
echo "Reference created at: $(date)"

# Running RSEM/STAR

echo "Starting RSEM/STAR at: $(date)"
python3 MASTERPROCESS_rsem_star.py ${USER_ID}
echo "Finished RSEM/STAR at: $(date)"

# Performing TMM normalization and .csv creation

conda env create -f /home/${USER_ID}/06-Integration_Project-main/2-Conda_envs/tmm_env.yml
conda activate tmm_env
cd /home/${USER_ID}/06-Integration_Project-main/5-QUANTIFY
echo "Starting TMM normalization and .csv creation at: $(date)"
Rscript create_TMM_matrix.R ${USER_ID}
echo "Finished TMM normalization and .csv creation at: $(date)"



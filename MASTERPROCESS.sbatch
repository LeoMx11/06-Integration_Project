#!/bin/bash

#SBATCH --job-name=MASTERPROCESS
#SBATCH --partition=batch
#SBATCH --output=mappo_%j.log
#SBATCH --error=mappo_%j.err
#SBATCH --time=36:00:00
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=leomcmahon@ucsb.edu  # optional

set -eo pipefail

# ---------- Activate your conda env without modules ----------
mkdir -p logs
# Point this to your Conda install:
if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
  source "$HOME/miniconda3/etc/profile.d/conda.sh"
elif [ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
  source "$HOME/anaconda3/etc/profile.d/conda.sh"
else
  echo "Could not find conda.sh; edit this sbatch to point at your Conda installation." >&2
  exit 1
fi

if [ -z "$1" ]; then
  echo "Usage: $0 <USER_ID>"
  exit 1
fi

echo "Starting at: $(date)"
bash MASTERPROCESS.sh "$1"
echo "Finished at: $(date)"

#!/bin/bash
#SBATCH --job-name=dorothy_filter
#SBATCH --partition=largemem
#SBATCH --output=trimmo_%j.log
#SBATCH --error=trimmo_%j.err
#SBATCH --time=36:00:00
#SBATCH --cpus-per-task=10
#SBATCH --mem=512G
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=leomcmahon@ucsb.edu  # optional

set -euo pipefail

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
conda activate trimmo

echo "Starting trimmomatic at: $(date)"
python3 trimmomatic.py
echo "Finished trimmomatic at: $(date)"

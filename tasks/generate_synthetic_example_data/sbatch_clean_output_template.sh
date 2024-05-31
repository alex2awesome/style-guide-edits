#!/bin/sh
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --time=20:00:00
#SBATCH --gres=gpu:1
#SBATCH --mem-per-gpu=100GB
#SBATCH --cpus-per-gpu=10
#SBATCH --partition=isi

python run_open_source_models.py \
  --model_id $1 \
  --prompt_type zeroshot \
  --clean_after_running \
  --clean_all_jsons_with_llm \
  --verbose

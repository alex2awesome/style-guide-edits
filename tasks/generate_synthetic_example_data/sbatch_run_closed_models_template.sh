#!/bin/sh
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --time=40:00:00
#SBATCH --gres=gpu:1
#SBATCH --mem-per-gpu=10GB
#SBATCH --cpus-per-gpu=10
#SBATCH --partition=isi

python run_synthetic_data_models.py  --model_id $1 --prompt_type $2 --input_file $3



#sbatch sbatch_run_models_template.sh gpt-4-turbo zeroshot_bad_only
#sbatch sbatch_run_models_template.sh gpt-3.5-turbo zeroshot_bad_only
sbatch sbatch_run_models_template.sh llama-3-70b zeroshot_cot_bad_only
sbatch sbatch_run_models_template.sh mixtral zeroshot_cot_bad_only
sbatch sbatch_run_models_template.sh command-r zeroshot_cot_bad_only

#sbatch sbatch_run_models_template.sh gpt-4-turbo zeroshot_pair
#sbatch sbatch_run_models_template.sh gpt-3.5-turbo zeroshot_pair
#sbatch sbatch_run_models_template.sh llama-3-70b zeroshot_pair
#sbatch sbatch_run_models_template.sh mixtral zeroshot_pair
#sbatch sbatch_run_models_template.sh command-r zeroshot_pair

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

sbatch $SCRIPT_DIR/../sbatch_scripts/sbatch_run_models_template.sh         llama-3-70b     zeroshot_cot_bad_only ../../corpora/buzzfeed/parsed-rules-df.csv
sbatch $SCRIPT_DIR/../sbatch_scripts/sbatch_run_models_template.sh         mixtral         zeroshot_cot_bad_only ../../corpora/buzzfeed/parsed-rules-df.csv
sbatch $SCRIPT_DIR/../sbatch_scripts/sbatch_run_models_template.sh         command-r       zeroshot_cot_bad_only ../../corpora/buzzfeed/parsed-rules-df.csv
sbatch $SCRIPT_DIR/../sbatch_scripts/sbatch_run_closed_models_template.sh  gpt-4-turbo     zeroshot_cot_bad_only ../../corpora/buzzfeed/parsed-rules-df.csv

##
sbatch $SCRIPT_DIR/../sbatch_scripts/sbatch_run_models_template.sh          llama-3-70b     zeroshot_cot_bad_only ../../corpora/guardian/parsed-rules-df.csv
sbatch $SCRIPT_DIR/../sbatch_scripts/sbatch_run_models_template.sh          mixtral         zeroshot_cot_bad_only ../../corpora/guardian/parsed-rules-df.csv
sbatch $SCRIPT_DIR/../sbatch_scripts/sbatch_run_models_template.sh          command-r       zeroshot_cot_bad_only ../../corpora/guardian/parsed-rules-df.csv
sbatch $SCRIPT_DIR/../sbatch_scripts/sbatch_run_closed_models_template.sh   gpt-4-turbo     zeroshot_cot_bad_only ../../corpora/guardian/parsed-rules-df.csv

##
sbatch $SCRIPT_DIR/../sbatch_scripts/sbatch_run_models_template.sh          llama-3-70b     zeroshot_cot_bad_only ../../corpora/mother_jones/parsed_rules.csv
sbatch $SCRIPT_DIR/../sbatch_scripts/sbatch_run_models_template.sh          mixtral         zeroshot_cot_bad_only ../../corpora/mother_jones/parsed_rules-df.csv
sbatch $SCRIPT_DIR/../sbatch_scripts/sbatch_run_models_template.sh          command-r       zeroshot_cot_bad_only ../../corpora/mother_jones/parsed_rules.csv
sbatch $SCRIPT_DIR/../sbatch_scripts/sbatch_run_closed_models_template.sh   gpt-4-turbo     zeroshot_cot_bad_only ../../corpora/mother_jones/parsed_rules.csv
##





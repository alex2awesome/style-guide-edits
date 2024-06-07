# style-guide-edits

This is the repository for the style-guides edits project.

`notebooks/` is where I've been exploring different prompting approaches to generate synthetic data.

`corpora/` is where the style guides I scraped are stored.

`tasks/` contains some scripts to run different parts of the wake/sleep cycle on the servers. This is an important directory to pay attention to as a lot of what happens in the notebooks is simply interpreting what got ran here. Here are the different files:

* `sbatch_meta_scripts` and `sbatch_scripts` are directories that contain the scripts I run. The `sbatch_meta_scripts` is the main one that I actually run. (`sbatch`, if you're not familiar, is a command-line tool for interacting with a shared, large computing resource https://centers.hpc.mil/users/docs/navy/nautilusSlurmGuide.html).
* `run_synthetic_data_models.py` is the main workhorse script that these other shell scripts are calling. It simply determines which prompts to use, which LLM to use, and which data to use, and puts it all together to run.
* `prompts.py`, the set of prompts I was experimenting with.
* `model_utils.py` contains helper functions, including functions to load models and run prompts through them.
* `run_json_parsing_models.py` checks the output of language models to at least make sure it can be parsed.
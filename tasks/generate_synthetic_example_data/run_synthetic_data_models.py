from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import pandas as pd
import prompts
import functools
import jsonlines
from tqdm.auto import tqdm
import os
import warnings
import re
import json
import ast
from model_util import get_model, model_map, default_proj_dir, prompt_model
from run_json_parsing_models import parse_datum

here = os.path.dirname(__file__)
warnings.simplefilter(action='ignore', category=SyntaxWarning)
default_rules_fn = os.path.join(here, '../../corpora/chicago-style-guide/all-rules.jsonl')


def _run_all_prompts(
        rule_title,
        rule_text,
        prompt_type,
        tokenizer,
        model,
        model_type,
        num_examples_to_generate,
        temperature,
        max_new_tokens,
        num_tries=5,
        clean_while_running=False,
        clean_all_jsons_with_llm=False
):
    if 'zeroshot' in prompt_type:
        if 'pair' in prompt_type:
            prompt = prompts.ZERO_SHOT_PAIR_SYNTHETIC_DATA
        elif 'cot' in prompt_type:
            prompt = prompts.ZERO_SHOT_COT_BAD_SYNTHETIC_DATA
        else:  # 'bad' in prompt_type:
            prompt = prompts.ZERO_SHOT_BAD_SYNTHETIC_DATA

    else:  # 'fewshot' in prompt_type:
        prompt = prompts.FEWSHOT_PROMPT

    messages = [
        # system_prompt,
        {
            'role': 'user',
            'content': prompt.format(
                style_guide_rule=rule_text,
                style_guide_rule_title=rule_title,
                n=num_examples_to_generate
            )
        }
    ]
    gen_output = None
    for _ in range(num_tries):
        try:
            gen_output = prompt_model(
                messages,
                tokenizer,
                model,
                model_type=model_type,
                temperature=temperature,
                max_new_tokens=max_new_tokens
            )
            if clean_while_running:
                gen_output = parse_datum(gen_output, correct_all_jsons_with_llm=clean_all_jsons_with_llm)
            return gen_output
        except Exception as e:
            print(f'Error: {e}')
    return gen_output


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_id', type=str, required=True)
    parser.add_argument('--input_file', type=str, default=default_rules_fn)
    parser.add_argument('--cache_dir', type=str, default=default_proj_dir)
    parser.add_argument('--prompt_type', type=str, default='zeroshot')
    parser.add_argument('--output_file', type=str, default=None)
    parser.add_argument('--num_examples_to_generate', type=int, default=10)
    parser.add_argument('--temperature', type=float, default=0.3)
    parser.add_argument('--max_new_tokens', type=int, default=1000)
    parser.add_argument('--num_tries', type=int, default=1)
    parser.add_argument('--clean_while_running', action='store_true')
    parser.add_argument('--clean_after_running', action='store_true')
    parser.add_argument(
        '--clean_all_jsons_with_llm',
        help="whether to clean all unparsable JSONs with LLM, or just the ones we can get some regex match with",
        action='store_true'
    )
    parser.add_argument('--verbose', action='store_true')

    args = parser.parse_args()
    if ('gpt' not in args.model_id) and (args.model_id not in model_map):
        raise ValueError(f"Model {args.model_id} not found in model map.")
    folder_name = os.path.dirname(args.input_file)
    folder_name = os.path.basename(folder_name)
    if args.output_file is None:
        args.output_file = f'{folder_name}__{args.model_id}_{args.prompt_type}.jsonl'

    if '.csv' in args.input_file:
        rules_to_use = pd.read_csv(args.input_file, index_col=0).fillna('')
        rules_to_use = rules_to_use.reset_index()
        rules_to_use['index'] = folder_name + '__' + rules_to_use['index'].astype(str)
    else:
        rules_to_use = pd.read_json(args.input_file, lines=True)
    print(json.dumps(vars(args), indent=4))

    all_messages = []
    tok_cutoff = 4000
    tokenizer, model, model_type = get_model(args.model_id, args.cache_dir)
    run_all_prompts = functools.partial(
        _run_all_prompts,
        prompt_type=args.prompt_type,
        tokenizer=tokenizer,
        model=model,
        num_examples_to_generate=args.num_examples_to_generate,
        temperature=args.temperature,
        max_new_tokens=args.max_new_tokens,
        model_type=model_type,
        num_tries=args.num_tries,
        clean_while_running=args.clean_while_running
    )

    f = jsonlines.open(args.output_file, 'a')
    one_col = rules_to_use.iloc[0]
    idx_col = 'url' if 'url' in one_col else 'index'
    title_col = 'title' if 'title' in one_col else 'rule_title'
    text_col = 'content' if 'content' in one_col else 'rule_text'

    for _, row in tqdm(rules_to_use.iterrows(), total=len(rules_to_use)):
        key = row[idx_col]
        rule_title = row[title_col]
        rule_text = row[text_col]

        if tok_cutoff != None:
            rule_toks = tokenizer.encode(rule_text)
            rule_text = tokenizer.decode(rule_toks[:tok_cutoff])

        f.write({
            'message': run_all_prompts(rule_title=rule_title, rule_text=rule_text),
            'key': key,
        })





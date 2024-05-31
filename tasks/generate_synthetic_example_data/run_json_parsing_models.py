import re
import json
import ast
from model_util import get_model
from tqdm.auto import tqdm
from model_util import default_proj_dir
import os
import pandas as pd
import prompts


p = re.compile(r'\[(.*)\]', flags=re.DOTALL)
tok, gpt_35_model, _ = get_model('gpt-3.5-turbo', cache_dir=None)
tok, gpt_4_model, _ = get_model('gpt-4-turbo', cache_dir=None)
WAS_UNCLEAR_STR = 'No clear rule or preference expressed.'


def correct_malformed_json(json_str, parse_list_or_dict='dict'):
    if parse_list_or_dict == 'dict':
        correction_prompt = prompts.FEW_SHOT_DICT_PARSING_PROMPT.format(json_str=json_str)
    else:
        correction_prompt = prompts.FEW_SHOT_LIST_PARSING_PROMPT.format(json_str=json_str)
    messages = [
        {
            "role": "system",
            "content": "You are a helpful coding editor."
        },
        {
            'role': 'user',
            'content': correction_prompt
        }
    ]
    output = gpt_4_model(messages=messages)
    corrected_json_str = output.choices[0].message.content
    corrected_json_str = re.search(p, corrected_json_str)
    return json_or_ast(corrected_json_str)


def robust_json(input_str):
    try:
        return json.loads(input_str)
    except:  # JSONDecodeError:
        return None


def robust_ast(input_str):
    try:
        return ast.literal_eval(input_str)
    except:
        return None


def json_or_ast(input_str):
    if input_str is None:
        return None
    return robust_json(input_str[0]) or robust_ast(input_str[0])


def parse_datum(datum, correct_all_jsons_with_llm=False, parse_list_or_dict='dict'):
    if WAS_UNCLEAR_STR in datum:
        return WAS_UNCLEAR_STR

    json_str = re.search(p, datum)
    parsed_json = json_or_ast(json_str)
    if correct_all_jsons_with_llm:
        if parsed_json is None:
            parsed_json = correct_malformed_json(datum, parse_list_or_dict=parse_list_or_dict)
    else:
        if (parsed_json is None) and (json_str is not None):
            parsed_json = correct_malformed_json(json_str[0], parse_list_or_dict=parse_list_or_dict)
    return parsed_json


def parse_data(
        data_df,
        col_to_clean='message',
        return_failed=False,
        verbose=False,
        correct_all_jsons_with_llm=False,
        parse_list_or_dict='dict'
):
    failed_parses = []
    parsed_output = []
    to_iterate = data_df[col_to_clean]
    if verbose:
        to_iterate = tqdm(to_iterate)
    for m in to_iterate:
        parsed_json = parse_datum(
            m, correct_all_jsons_with_llm=correct_all_jsons_with_llm,
            parse_list_or_dict=parse_list_or_dict
        )
        if parsed_json is None:
            failed_parses.append(m)
        parsed_output.append(parsed_json)
    if return_failed:
        return parsed_output, failed_parses
    return parsed_output


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_id', type=str, required=True)
    parser.add_argument('--input_file', type=str, default=None)
    parser.add_argument('--gen_text_col', type=str, default='message')
    parser.add_argument('--cache_dir', type=str, default=default_proj_dir)
    parser.add_argument('--temperature', type=float, default=0.3)
    parser.add_argument('--max_new_tokens', type=int, default=1000)
    parser.add_argument('--num_tries', type=int, default=1)
    parser.add_argument(
        '--clean_all_jsons_with_llm',
        help="whether to clean all unparsable JSONs with LLM, or just the ones we can get some regex match with",
        action='store_true'
    )
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    if args.input_file is None:
        args.input_file = f'{args.model_id}_{args.prompt_type}.jsonl'

    if not os.path.exists(args.input_file):
        raise ValueError(f"Output file {args.input_file} does not exist.")

    parse_type = 'list' if 'bad_only' in args.input_file else 'dict'

    ## read in the data
    data_df = pd.read_json(args.input_file, lines=True)
    parsed_output = parse_data(
        data_df,
        col_to_clean=args.gen_text_col,
        correct_all_jsons_with_llm=args.clean_all_jsons_with_llm,
        verbose=args.verbose,
        parse_list_or_dict=parse_type
    )
    data_df['parsed_output'] = parsed_output
    data_df.to_json(args.input_file, lines=True)
    exit()


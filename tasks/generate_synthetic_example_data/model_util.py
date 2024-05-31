import os
from openai import OpenAI
import functools
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


default_proj_dir = "/project/jonmay_231/spangher/huggingface_cache"
model_map = {
    'llama-2-7b': 'togethercomputer/Llama-2-7B-32K-Instruct',
    'llama-2-70b': 'upstage/Llama-2-70b-instruct',
    'llama-3-8b': 'meta-llama/Meta-Llama-3-8B-Instruct',
    'llama-3-70b': 'meta-llama/Meta-Llama-3-70B-Instruct',
    'mixtral': "mistralai/Mixtral-8x7B-Instruct-v0.1",
    'command-r': "CohereForAI/c4ai-command-r-v01",
}


def get_model(model_name, cache_dir):
    ## openai model
    if 'gpt' in model_name:
        key_path = os.path.expanduser('~/.openai-isi-key.txt')
        client = OpenAI(api_key=open(key_path).read().strip())
        model = functools.partial(client.chat.completions.create, model=model_name)
        tokenizer = AutoTokenizer.from_pretrained('gpt2')
        return tokenizer, model, 'openai'
    else:
        ## huggingface model
        model_id = model_map[model_name]
        tokenizer = AutoTokenizer.from_pretrained(model_id, cache_dir=cache_dir)
        model = AutoModelForCausalLM.from_pretrained(
            model_id, cache_dir=cache_dir, torch_dtype=torch.bfloat16, device_map='auto'
        )
        model.eval()
        return tokenizer, model, 'hf'


## conduct real prompts
def prompt_model(messages, tokenizer, model, model_type, temperature, max_new_tokens):
    ## huggingface
    if model_type == 'hf':
        input_ids = tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to('cuda')

        # <BOS_TOKEN><|START_OF_TURN_TOKEN|><|USER_TOKEN|>Hello, how are you?<|END_OF_TURN_TOKEN|><|START_OF_TURN_TOKEN|><|CHATBOT_TOKEN|>
        gen_tokens = model.generate(
            input_ids,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=temperature,
        )
        return tokenizer.decode(gen_tokens[0, input_ids.shape[1]:])
    else:
        ## openai
        response = model(
            messages=messages,
            temperature=temperature,
            max_tokens=max_new_tokens,
        )
        return response.choices[0].message.content


def batchify(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


def prompt_model_stacked(data_df, tokenizer, model, model_type, temperature, max_new_tokens, num_tries):
    pass

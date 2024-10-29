import argparse
import yaml
import sys

from base_data_collector import get_files
from custom_data_collector import SimpleSplitDataSampler
import pandas as pd

from transformers import AutoModelForCausalLM, AutoTokenizer


def main(yaml_file):
    
    # Create dataset 

    with open(yaml_file) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    py_files = get_files(
        dir=config['generate_data']['dir_load'], 
        extension=config['generate_data']['extension'], 
        filter_regex=config['generate_data']['filter_regex'],
        min_lines=config['generate_data']['min_lines'],
    )

    sampler = SimpleSplitDataSampler(
        py_files, 
        max_prefix=config['generate_data']['max_prefix'],
        max_middle=config['generate_data']['max_middle'],
        max_suffix=config['generate_data']['max_suffix'],
        splitters=config['generate_data']['splitters'],
    )

    path_load = config['generate_data']['path_load']
    datasets = [] if path_load is None else [pd.read_parquet(path_load).drop('output', axis=1)]

    for d in config['generate_data']['datasets']:
        datasets.append(sampler.sample(**d))

    dataset = pd.concat(datasets, ignore_index=True)
    dataset['query'] = (
        '<fim_prefix>' + dataset['prefix'] + 
        '<fim_suffix>' + dataset['suffix'] + 
        '<fim_middle>'
    )

    # Generate middles

    checkpoint = config['model']['checkpoint']
    device = config['model']['device']
    max_new_tokens = config['model']['max_new_tokens']

    tokenizer = AutoTokenizer.from_pretrained(checkpoint, clean_up_tokenization_spaces=True)
    model = AutoModelForCausalLM.from_pretrained(checkpoint).to(device)

    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = 'left'
    inputs, masks = tokenizer(dataset['query'].to_list(), padding=True, return_tensors='pt').values()
    inputs = inputs.to(device)
    masks = masks.to(device)

    outputs = model.generate(inputs, attention_mask=masks, max_new_tokens=max_new_tokens)
    outputs_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    lengths = dataset['prefix'].str.len() + dataset['suffix'].str.len()

    dataset['output'] = [output[length:] for output, length in zip(outputs_text, lengths)]

    dataset.to_parquet(config['generate_data']['path_save'])


if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print("Usage: python generater.py <path_to_yaml_file>")
        sys.exit(1)

    parser = argparse.ArgumentParser(description='Generate dataset and test a model using yaml config.')
    parser.add_argument('yaml_file', type=str, help='Path to the YAML file')
    args = parser.parse_args()

    main(args.yaml_file)

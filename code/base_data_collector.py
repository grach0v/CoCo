import os
import re
from typing import List, Tuple, Union

import numpy as np
import pandas as pd


def get_files(
        dir: Union[str, os.PathLike], 
        extension: str, 
        filter_regex: str = '.*', 
        min_lines: int = 0,
    ) -> List[str]:
    """
    Recursively searches for files with a given extension in a directory and filters lines based on a regex pattern.

    Args:
        dir (str): The directory to search in.
        extension (str): The file extension to look for.
        filter_regex (str): The regex pattern to filter lines. Defaults to '*'.
        min_lines (int): The minimum number of matching lines required to include the file. Defaults to 0.

    Returns:
        List[str]: A list of file paths that match the criteria.
    """
    py_files = []
    pattern = re.compile(filter_regex)

    for root, _, files in os.walk(dir):
        for file in files:
            if file.endswith(extension):
                full_path = os.path.join(root, file)

                with open(full_path, 'r') as file:
                    lines = [line for line in file if pattern.search(line)]

                if len(lines) > min_lines:
                    py_files.append(full_path)
    
    return py_files

class BaseDataSampler:
    def __init__(
            self, 
            files: List[str], 
            max_prefix: int, 
            max_middle: int, 
            max_suffix: int
        ):
        """
        Initializes the BaseDataSampler with the given files and maximum lengths for prefix, middle, and suffix.

        Args:
            files (List[str]): List of file paths to sample from.
            max_prefix (int): Maximum length of the prefix.
            max_middle (int): Maximum length of the middle part.
            max_suffix (int): Maximum length of the suffix.
        """

        self.files = files
        self.max_prefix = max_prefix
        self.max_middle = max_middle
        self.max_suffix = max_suffix

    def sample(
            self, 
            num_files: int, 
            replace: bool = True, 
            strategy: str = None, 
            strategy_args: List = [], 
            strategy_kwargs: dict = {},
            return_failed_files: bool = False,
        ) -> Union[pd.DataFrame, Tuple[pd.DataFrame, List[str]]]:
        """
        Samples data from the files using a specified strategy.

        Args:
            num_files (int): Number of files to sample.
            replace (bool): Whether to sample with replacement. Defaults to True.
            strategy (str): The strategy to use for sampling.
            strategy_args (List): Arguments for the strategy function.
            strategy_kwargs (dict): Keyword arguments for the strategy function.
            return_failed_files (bool): Whether to return failed files. Defaults to False.

        Returns:
            Union[pd.DataFrame, Tuple[pd.DataFrame, List[str]]]: The sampled dataset and optionally the failed files.
        """
        chosen_files = np.random.choice(self.files, num_files, replace=replace)

        dataset = {
            'filename': chosen_files,
            'prefix': [],
            'middle': [],
            'suffix': [],
            'meta': [],
        }

        failed_files = []

        for filename in chosen_files:
            with open(filename, 'r') as file:
                lines = file.readlines()

            if not hasattr(self, strategy):
                raise AttributeError(f'Strategy {strategy} was not provided')
            
            success, prefix, middle, suffix, meta = getattr(self, strategy)(lines, *strategy_args, **strategy_kwargs)            
            
            if success:
                dataset['prefix'].append(prefix)
                dataset['middle'].append(middle)
                dataset['suffix'].append(suffix)
                dataset['meta'].append(meta)
            else:
                failed_files.append(filename)

        dataset = pd.DataFrame(dataset)

        if return_failed_files:
            return dataset, failed_files
        
        return dataset